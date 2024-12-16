from typing import TypeVar, Generic

from pydantic import BaseModel, TypeAdapter

ContainerT = TypeVar('DataT')

class PaginatedResultSet(BaseModel, Generic[ContainerT]):
    offset: int
    limit: int
    objects: ContainerT


class Book(BaseModel):
    title: str
    path: str


BookList = TypeAdapter(list[Book])
