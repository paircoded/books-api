from books_api.persist.utils import get_db_session
from books_api.types import Book, BookList, PaginatedResultSet


async def list_books(offset=0, limit=25) -> PaginatedResultSet[Book]:
    with get_db_session() as session:
        db_data = await session.scalars(Book).offset(offset).limit(limit).all()

    return PaginatedResultSet[Book](
        offset=offset,
        limit=limit,
        objects=BookList.model_validate(db_data)
    )
