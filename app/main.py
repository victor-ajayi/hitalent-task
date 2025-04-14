from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.routers.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Hitalent Junior Developer Task",
    docs_url=None if not settings.DEBUG else "/docs",
    redoc_url=None,
    lifespan=lifespan,
)

app.include_router(api_router, prefix="")
