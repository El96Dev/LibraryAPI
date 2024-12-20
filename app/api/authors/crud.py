from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .schemas import AuthorBase, AuthorGet
from .dependencies import get_author_by_id
from core.models import Author



async def create_author(new_author: AuthorBase, session: AsyncSession) -> AuthorGet:
    author_db = Author(**new_author.model_dump())
    session.add(author_db)
    await session.commit()
    return author_db

async def get_authors(session: AsyncSession) -> list[AuthorGet]:
    stmt = select(Author)
    result = await session.execute(stmt)
    authors = result.scalars().all()
    return authors

async def get_author(author_id: int, session: AsyncSession) -> AuthorGet | None:
    author = await get_author_by_id(author_id, session)
    return author

async def update_author(author_id: int, author_update: AuthorBase, session: AsyncSession) -> Author | None:
    author = await get_author_by_id(author_id, session)
    if author is not None:
        author.firstname = author_update.firstname
        author.lastname = author_update.lastname
        author.birth_date = author_update.birth_date
        await session.commit()
        return author
    
async def delete_author(author_id: int, session: AsyncSession) -> None:
    author = await get_author_by_id(author_id, session)
    if author is not None:
        await session.delete(author)
        await session.commit()