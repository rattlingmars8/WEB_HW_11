from pydantic import BaseModel, validator, EmailStr
from datetime import datetime, date


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    b_day: date
    rest_data: str = None

    @validator('b_day')
    def validate_b_day(cls, b_day):
        today = date.today()
        if b_day > today:
            raise ValueError('Birthday cannot be in the future')
        try:
            datetime.strftime(b_day, '%Y-%m-%d')
        except:
            raise ValueError('Incorrect date format. Please use "YYYY-MM-DD".')
        return b_day


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int = 1

    class Config:
        orm_mode = True
