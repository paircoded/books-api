from typing import TypeVar, Generic

from pydantic import BaseModel, TypeAdapter

DataT = TypeVar('DataT')

class PaginatedResultSet(BaseModel, Generic[DataT]):
    offset: int
    limit: int
    objects: list[DataT]


class Book(BaseModel):
    title: str
    path: str


BookList = TypeAdapter(list[Book])
