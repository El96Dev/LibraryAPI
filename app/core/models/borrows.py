from datetime import date

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Borrow(Base):
    __tablename__ = "borrows"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    reader: Mapped[str] = mapped_column(String)
    issue_date: Mapped[date] = mapped_column(Date)
    return_date: Mapped[date] = mapped_column(Date, nullable=True)