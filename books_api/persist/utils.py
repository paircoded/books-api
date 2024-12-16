from contextlib import contextmanager

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from books_api.settings import settings


@contextmanager
async def get_db_session():
    engine = create_async_engine(settings.sqlalchemy_url)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
