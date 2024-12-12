from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .schemas import BookBase, BookGet
from .dependencies import get_book_by_id
from core.models import Book
from ..authors.dependencies import get_author_by_id


async def create_book(new_book: BookBase, session: AsyncSession) -> BookGet | None:
    try:
        author = await get_author_by_id(new_book.author_id, session)
        if author is not None:
            book_db = Book(**new_book.model_dump())
            session.add(book_db)
            await session.commit()
            return book_db
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer!")
    

async def get_books(session: AsyncSession) -> list[BookGet]:
    stmt = select(Book)
    result = await session.execute(stmt)
    books = result.scalars().all()
    return books

async def get_book(book_id: int, session: AsyncSession) -> BookGet | None:
    book = await get_book_by_id(book_id, session)
    return book

async def update_book(book_id: int, book_update: BookBase, session: AsyncSession) -> BookGet | None:
    try:
        book = await get_book_by_id(book_id, session)
        if book is not None:
            book.author_id = book_update.author_id
            book.title = book_update.title
            book.description = book_update.description
            book.quantity = book_update.quantity
            await session.commit()
            return book
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer!")

async def delete_book(book_id: int, session: AsyncSession) -> None:
    book = await get_book_by_id(book_id, session)
    if book is not None:
        await session.delete(book)
        await session.commit()