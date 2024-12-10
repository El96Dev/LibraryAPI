from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import Author


async def get_author_by_id(author_id: int, session: AsyncSession) -> Author | None:
    stmt = select(Author).where(Author.id==author_id)
    result = await session.execute(stmt)
    author = result.scalars().one_or_none()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {author_id} wasn't found!")
    else:
        return author