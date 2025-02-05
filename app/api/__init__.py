from fastapi import APIRouter

from config import settings


api_router = APIRouter(prefix=settings.api.prefix)
template_router = APIRouter()


from .user import router as user_router
api_router.include_router(user_router)

from .html_files import router as templates_router
template_router.include_router(templates_router)