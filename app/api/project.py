from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import ValidationError

from config import settings
from app import db_helper
from app.dao import project as project_dao
from app.models.project import Project
from app.schemas.project import ProjectAddData, AllProjectsData

router: APIRouter = APIRouter(prefix=settings.api.project_prefix)

@router.get("/all", response_model=AllProjectsData)
async def submit_form(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    projects: AllProjectsData = await project_dao.get_all_projects(session=session)
    print("Это ПРОООООООООООООООООООЕКТТТТТТТТТТТЫЫЫЫЫЫЫЫЫЫ", projects)
    return projects
