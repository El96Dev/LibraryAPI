from datetime import date

from pydantic import BaseModel


class BorrowBase(BaseModel):
    book_id: int
    reader: str
    issue_date: date


class BorrowGet(BorrowBase):
    id: int
    return_date: date | None


class BorrowUpdate(BaseModel):
    return_date: date
