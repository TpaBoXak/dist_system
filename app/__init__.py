from fastapi import FastAPI
from config import settings
from contextlib import asynccontextmanager
from app.models import DataBaseHelper


db_helper = DataBaseHelper(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print(str(settings.db.url))
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


app = FastAPI()

from app.api import api_router
app.include_router(api_router)

from app.api import template_router
app.include_router(template_router)

