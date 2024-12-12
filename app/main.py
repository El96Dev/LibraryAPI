import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.models import db_helper
from api import router


app = FastAPI()
app.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)


