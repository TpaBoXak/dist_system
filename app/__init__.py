from fastapi import FastAPI
from config import settings
from contextlib import asynccontextmanager

app = FastAPI()

from app.api import api_router
app.include_router(api_router)

from app.api import template_router
app.include_router(template_router)

