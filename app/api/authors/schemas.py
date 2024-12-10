from pydantic import BaseModel


class AuthorBase(BaseModel):
    firstname: str
    lastname: str
    birth_date: str


