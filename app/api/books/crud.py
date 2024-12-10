from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas import BookBase
from core.models import Book
from dependencies import get_book_by_id
from authors.dependencies import get_author_by_id


async def create_book(new_book: BookBase, session: AsyncSession) -> BookBase | None:
    try:
        author = await get_author_by_id(new_book.author_id, session)
        if author is not None:
            book_db = Book(**new_book.model_dump())
            session.add(book_db)
            await session.commit()
            return book_db
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer")
    

async def get_books(session: AsyncSession) -> list[BookBase]:
    stmt = select(Book)
    result = await session.execute(stmt)
    books = result.scalars().all()
    return books

async def get_book(book_id: int, session: AsyncSession) -> BookBase | None:
    book = await get_book_by_id(book_id, session)
    return book

async def update_book(book_id: int, book_update: BookBase, session: AsyncSession) -> BookBase | None:
    try:
        book = await get_book_by_id(book_id, session)
        if book is not None:
            for key, value in book_update.items():
                setattr(book, key, value)
            await session.commit()
            return book
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer")

async def delete_book(book_id: int, session: AsyncSession) -> None:
    book = await get_book_by_id(book_id, session)
    if book is not None:
        await session.delete(book)
        await session.commit()