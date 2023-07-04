from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from src.DB.db import get_db
from src.routes import contacts

app = FastAPI()
app.include_router(contacts.router, tags=["contacts"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker", tags=["Root"])
async def healthchecker(session: AsyncSession = Depends(get_db)):
    try:
        result = await session.execute(text("SELECT 1"))
        rows = result.fetchall()
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "You successfully connected to the database!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )
