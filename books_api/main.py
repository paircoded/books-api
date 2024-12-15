from typing import Union

from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from books_api.auth.dependencies import account_access_token

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


@app.get("/")
def list_home_data():
    return {"hello": "world"}


@app.get("/items/{item_id}", dependencies=[Depends(account_access_token)])
def create_book(item_id: int, q: Union[str, None] = None):
    return {"books": item_id, "q": q}


@app.post("/books/upload", dependencies=[Depends(account_access_token)])
def upload_book(file: UploadFile):
    return {"filename": file.filename}
