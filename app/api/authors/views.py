from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .schemas import AuthorBase, AuthorGet
from . import crud


router = APIRouter(tags=["Authors"])

@router.get("")
async def get_authors(session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> list[AuthorGet]:
    authors = await crud.get_authors(session)
    return authors

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(new_author: AuthorBase, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> AuthorGet:
    author = await crud.create_author(new_author, session)
    return author

@router.get("/{author_id}")
async def get_author(author_id: int, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> AuthorGet | None:
    author = await crud.get_author(author_id, session)
    return author

@router.put("/{author_id}")
async def update_author(author_id: int, author_update: AuthorBase, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> AuthorGet | None:
    author = await crud.update_author(author_id, author_update, session)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int, session: AsyncSession=Depends(db_helper.scoped_session_dependency)) -> None:
    await crud.delete_author(author_id, session)