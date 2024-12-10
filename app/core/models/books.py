from sqlalchemy import String, Text, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text) 
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    quantity: Mapped[int] = mapped_column(Integer, CheckConstraint("quantity >= 0"))