from books_api.types import Book, BookList, PaginatedResultSet


async def list_books(db_session, offset=0, limit=25) -> PaginatedResultSet[Book]:
    db_data = await db_session.scalars(Book).offset(offset).limit(limit).all()

    return PaginatedResultSet[Book](
        offset=offset, limit=limit, objects=BookList.model_validate(db_data)
    )
