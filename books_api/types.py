import uuid
from typing import TypeVar, Generic

from pydantic import BaseModel, ConfigDict

DataT = TypeVar("DataT")


class PaginatedResultSet(BaseModel, Generic[DataT]):
    offset: int
    limit: int
    objects: list[DataT]


class Book(BaseModel):
    id: uuid.UUID
    title: str
    upload_path: str

    model_config = ConfigDict(from_attributes=True)
