from fastapi import APIRouter

from core.config import settings
from .authors.views import router as authors_router
from .books.views import router as books_router
from .borrows.views import router as borrows_router


router = APIRouter()
router.include_router(authors_router, prefix=settings.api.authors)
router.include_router(books_router, prefix=settings.api.books)
router.include_router(borrows_router, prefix=settings.api.borrows)