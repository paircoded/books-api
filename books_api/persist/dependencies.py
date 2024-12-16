from typing import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from books_api.persist import utils
from books_api.settings import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    yield await utils.get_db_session()
