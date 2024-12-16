import hashlib
import os
import uuid
from typing import Annotated

from fastapi import FastAPI, Depends, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from books_api import services
from books_api.auth.dependencies import account_access_token
from books_api.persist import models
from books_api.persist.dependencies import get_db_session, get_repository
from books_api.persist.repository import DatabaseRepository
from books_api.services import save_uploaded_book
from books_api.settings import settings
from books_api.types import PaginatedResultSet, Book

app = FastAPI()

origins = [
    "https://books-api.paircoded.com",
    "https://books.paircoded.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BookRepository = Annotated[
    DatabaseRepository[models.Book],
    Depends(get_repository(models.Book)),
]


@app.get("/books", dependencies=[Depends(account_access_token)], status_code=status.HTTP_201_CREATED)
async def list_books(
        offset: int = 0,
        limit: int = 25,
        db_session: AsyncSession = Depends(get_db_session),
) -> PaginatedResultSet[Book]:
    return await services.list_books(db_session, offset=offset, limit=limit)


@app.post("/books/upload", dependencies=[Depends(account_access_token)], response_model=Book,
          response_model_exclude={'path'})
async def upload_book(
        file: UploadFile,
        repository: BookRepository
):
    filename_hash = hashlib.md5(file.filename.encode('utf-8')).hexdigest()
    filename = f"{filename_hash}.epub"
    output_file_path = os.path.join(settings.book_storage_base_directory, filename)
    with open(output_file_path, "wb") as output_file:
        output_file.write(file.file.read())
    book = Book(
        id=uuid.uuid4(),
        title=file.filename,
        path=output_file_path,
    )

    repository.create(book)
