import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_, and_, extract, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.DB.models import Contact
from utils.CRUD import create_contact, get_contacts, get_contact, update_contact, delete_contact
from src.DB.db import get_db
from src.schemas import ContactCreate, ContactResponse, ContactUpdate

router = APIRouter(prefix='/contacts', tags=["contacts"])


# CRUD block
@router.get("/", tags=["contacts"], response_model=list[ContactResponse])
async def get_contacts_db(limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await get_contacts(limit, offset, db)


@router.get("/{id}", tags=["contacts"], response_model=ContactResponse)
async def get_contact_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_contact(id, db)


@router.post("/", tags=["contacts"], response_model=ContactResponse)
async def create_new_contact(body: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await create_contact(body, db)


@router.put("/{id}", tags=["contacts"], response_model=ContactResponse)
async def update_contact_db(id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)):
    return await update_contact(id, body, db)


@router.delete("/{id}", tags=["contacts"])
async def delete_contact_db(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_contact(id, db)


# end of CRUD block

"""Additional block
Контакти повинні бути доступні для пошуку за ім'ям, прізвищем або адресою електронної пошти (Query)."""


@router.get("/query/", tags=["contacts"], response_model=list[ContactResponse])
async def get_contacts_query(
        limit: int = 100,
        offset: int = 0,
        query: Optional[str] = Query(None, min_length=2, max_length=100),
        db: AsyncSession = Depends(get_db)
):
    print(len(await get_contacts(limit, offset, db, query)))
    return await get_contacts(limit, offset, db, query)


"""API повинен мати змогу отримати список контактів з днями народження на найближчі 7 днів."""


@router.get("/upcoming_birthdays/", tags=["contacts"], response_model=list[ContactResponse])
async def get_upcoming_birthday_contacts(limit: int = 100, db: AsyncSession = Depends(get_db)):
    today = datetime.datetime.now().date()
    end_date = today + datetime.timedelta(days=7)

    stmt = (
        select(Contact)
        .where(
            or_(
                and_(
                    extract('month', Contact.b_day) == today.month,
                    extract('day', Contact.b_day) >= today.day
                ),
                and_(
                    extract('month', Contact.b_day) == end_date.month,
                    extract('day', Contact.b_day) <= end_date.day
                )
            )
        ).limit(limit)
    ).order_by(asc(Contact.id))

    result = await db.execute(stmt)
    return result.scalars().all()
