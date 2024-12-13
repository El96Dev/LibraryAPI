from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Borrow, Book


async def get_borrow_by_id(borrow_id: int, session: AsyncSession) -> Borrow | None:
    stmt = select(Borrow).where(Borrow.id==borrow_id)
    result = await session.execute(stmt)
    borrow = result.scalars().one_or_none()
    if not borrow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Borrow with id {borrow_id} wasn't found!")
    else:
        return borrow

async def get_book_quantity(book_id: int, session: AsyncSession) -> int | None:
    stmt = select(Book).where(Book.id==book_id)
    result = await session.execute(stmt)
    book = result.scalars().one_or_none()
    if book is not None:
        return book.quantity
    else:
        print(f"No book found {book_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} wasn't found!")
    
async def get_book_by_id(book_id: int, session: AsyncSession) -> Book | None:
    stmt = select(Book).where(Book.id==book_id)
    result = await session.execute(stmt)
    book = result.scalars().one_or_none()
    if book is not None:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} wasn't found!")