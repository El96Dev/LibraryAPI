from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import Book


async def get_book_by_id(book_id: int, session: AsyncSession) -> Book | None:
    stmt = select(Book).where(Book.id==book_id)
    result = await session.execute(stmt)
    book = result.scalars().one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} wasn't found!")
    else:
        return book
    