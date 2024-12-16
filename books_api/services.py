from sqlalchemy import select

from books_api.persist import models
from books_api.types import Book, PaginatedResultSet


async def list_books(db_session, offset=0, limit=25) -> PaginatedResultSet[Book]:
    db_data = await db_session.scalars(select(models.Book).offset(offset).limit(limit))
    books = [Book.model_validate(row) for row in db_data]
    return PaginatedResultSet[Book](offset=offset, limit=limit, objects=books)
