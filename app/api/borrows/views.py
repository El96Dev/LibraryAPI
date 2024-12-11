from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from core.models import db_helper
from schemas import BorrowBase, BorrowGet, BorrowUpdate


router = APIRouter()

@router.get("")
async def get_borrows(session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> list[BorrowGet]:
    borrows = await crud.get_borrows(session)
    return borrows

@router.get("/{borrow_id}")
async def get_borrow(borrow_id: int, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> BorrowGet | None:
    borrow = await crud.get_borrow(borrow_id, session)
    return borrow

@router.post("")
async def create_borrow(new_borrow: BorrowBase, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> BorrowGet | None:
    borrow = await crud.create_borrow(new_borrow, session)
    return borrow

@router.patch("/{borrow_id}")
async def update_borrow(borrow_id: int, borrow_update: BorrowUpdate, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> BorrowGet | None:
    borrow = await crud.update_borrow(borrow_id, borrow_update, session)
    return borrow