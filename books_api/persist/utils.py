from contextlib import asynccontextmanager

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from books_api.settings import settings


# def get_db_session():
#     engine = create_async_engine(settings.sqlalchemy_url)
#     return factory = async_sessionmaker(engine)
