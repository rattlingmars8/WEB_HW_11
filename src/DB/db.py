import configparser
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

config_ini = Path(__file__).parent.parent.joinpath("conf/config.ini")

config = configparser.ConfigParser()

config.read(config_ini)

user = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")
host = config.get("DB", "HOST")
port = config.get("DB", "PORT")
db_name = config.get("DB", "DB")

URL = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'

engine = create_async_engine(URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
