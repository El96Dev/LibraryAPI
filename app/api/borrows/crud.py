from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Borrow
from .schemas import BorrowBase, BorrowGet, BorrowUpdate
from .dependencies import get_borrow_by_id, get_book_quantity, get_book_by_id
from ..books.dependencies import get_book_by_id


async def get_borrow(borrow_id: int, session: AsyncSession) -> BorrowGet | None:
    borrow = await get_borrow_by_id(borrow_id, session)
    return borrow

async def get_borrows(session: AsyncSession) -> list[BorrowGet]:
    stmt = select(Borrow)
    result = await session.execute(stmt)
    borrows = result.scalars().all()
    return borrows

async def update_borrow(borrow_id: int, borrow_update: BorrowUpdate, session: AsyncSession) -> BorrowGet | None:
    borrow = await get_borrow_by_id(borrow_id, session)
    book = await get_book_by_id(borrow.book_id, session)
    if borrow.return_date is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Return date is already set!")
    if borrow.issue_date > borrow_update.return_date:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The return date must be later than the issue date!")
    if borrow is not None:
        book.quantity += 1
        borrow.return_date = borrow_update.return_date
        await session.commit()
        return borrow

async def create_borrow(new_borrow: BorrowBase, session: AsyncSession) -> BorrowGet | None:
    book_quantity = await get_book_quantity(new_borrow.book_id, session)
    if book_quantity == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Library is out of book with id {new_borrow.book_id}!")
    borrow_db = Borrow(**new_borrow.model_dump())
    session.add(borrow_db)
    book = await get_book_by_id(new_borrow.book_id, session)
    book.quantity -= 1
    await session.commit()
    return borrow_db

