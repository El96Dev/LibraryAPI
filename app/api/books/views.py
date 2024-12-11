from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper
from .schemas import BookBase


router = APIRouter(tags=["Books"])

@router.get("")
async def get_books(session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> list[BookBase]:
    books = await crud.get_books(session)
    return books

@router.post("")
async def create_book(new_book: BookBase, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> BookBase | None:
    book = await crud.create_book(new_book, session)
    return book

@router.get("/{book_id}")
async def get_book(book_id: int, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> BookBase | None:
    book = await crud.get_book_by_id(book_id, session)
    return book

@router.put("/{book_id}")
async def update_book(book_id: int, book_update: BookBase, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> BookBase | None:
    book = await crud.update_book(book_id, book_update, session)
    return book    

@router.delete("/{book_id}")
async def delete_book(book_id: int, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> None:
    await crud.delete_book(book_id, session)
