import hashlib
import os
import uuid

from sqlalchemy import select

from books_api.persist import models
from books_api.persist.repository import DatabaseRepository
from books_api.settings import settings
from books_api.types import Book, PaginatedResultSet


async def list_books(db_session, offset=0, limit=25) -> PaginatedResultSet[Book]:
    db_data = await db_session.scalars(select(models.Book).offset(offset).limit(limit))
    books = [Book.model_validate(row) for row in db_data]
    return PaginatedResultSet[Book](offset=offset, limit=limit, objects=books)


async def save_uploaded_book(repository: DatabaseRepository[models.Book], file) -> Book:
    filename_hash = hashlib.md5(file.filename.encode("utf-8")).hexdigest()
    filename = f"{filename_hash}.epub"
    output_file_path = os.path.join(settings.book_storage_base_directory, filename)
    with open(output_file_path, "wb") as output_file:
        output_file.write(file.file.read())

    book = Book(
        id=uuid.uuid4(),
        title=file.filename,
        path=output_file_path,
    )

    db_book = await repository.create(book.model_dump())
    return Book.model_validate(db_book)
