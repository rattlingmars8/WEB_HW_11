from sqlalchemy import Column, Integer, String, Date, Text, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    b_day = Column(Date, nullable=False)
    rest_data = Column(Text, nullable=True)
