from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    description: str
    author_id: int
    quantity: int
