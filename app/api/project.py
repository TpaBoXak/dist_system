from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import ValidationError

from typing import Optional

from config import settings
from app import db_helper
from app.dao import project as project_dao
from app.dao import users as user_dao
from app.models.project import Project
from app.schemas.project import ProjectAddData, AllProjectsData

router: APIRouter = APIRouter(prefix=settings.api.project_prefix)

@router.get("/all", response_model=AllProjectsData)
async def submit_form(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    projects: AllProjectsData = await project_dao.get_all_projects(session=session)
    return projects


@router.post("/add")
async def add_project(
    project_data: ProjectAddData,
    user_id: int = Header(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if not await user_dao.is_gip(session=session, user_id=user_id):
        raise HTTPException(status_code=404, detail="Have not rights")
    
    project_id: Optional[int] = await project_dao.add_project(
        session=session, owner_id=user_id, project_data=project_data
    )

    if project_id is None:
        raise HTTPException(status_code=500,
            detail="Ошибка Добавления проекта")
    
    if not await project_dao.add_worker(
        session=session,
        workers_ids=project_data.workers,
        project_id=project_id
    ):
        await project_dao.delete_project(
            session=session,
            project_id=project_id
        )
        raise HTTPException(status_code=500,
            detail="Ошибка Добавления работников в проект")
