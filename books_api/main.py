from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from books_api import services
from books_api.auth.dependencies import account_access_token
from books_api.persist.dependencies import get_db_session
from books_api.services import save_uploaded_book
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


@app.get("/books", dependencies=[Depends(account_access_token)])
async def list_books(
        offset: int = 0,
        limit: int = 25,
        db_session: AsyncSession = Depends(get_db_session),
) -> PaginatedResultSet[Book]:
    return await services.list_books(db_session, offset=offset, limit=limit)



@app.post("/books/upload", dependencies=[Depends(account_access_token)], response_model=Book, response_model_exclude={'path'})
async def upload_book(
        file: UploadFile,
        db_session: AsyncSession = Depends(get_db_session),
):
    return await save_uploaded_book(db_session, file)
