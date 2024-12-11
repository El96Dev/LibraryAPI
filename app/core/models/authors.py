from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, ForeignKey

from .base import Base


class Author(Base):
    __tablename__ = "authors"

    firstname: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    birth_date: Mapped[date] = mapped_column(Date)
