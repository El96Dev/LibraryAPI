from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    firstname: str
    lastname: str
    birth_date: date


class AuthorGet(AuthorBase):
    id: int


