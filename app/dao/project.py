from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

from sqlalchemy import select
from sqlalchemy import func

from typing import Optional

from app.schemas.project import AllProjectsData, ProjectData, ProjectAddData
from app.schemas.user import LightWorker
from app.schemas.prof import ExperianceData
from app.models.project import Project, ProjectWorker
from app.models.profession import Experience, Profession
from app.dao import users as users_dao


async def get_all_projects(
    session: AsyncSession,
) -> AllProjectsData:
    stmt = select(
        Project.id, User.first_name, User.second_name,
        Project.title, Project.desc, func.count(ProjectWorker.id)
    ).select_from(Project).join(User, Project.owner_id == User.id).\
    join(ProjectWorker, Project.id == ProjectWorker.project_id).\
    group_by(Project.id, User.first_name, User.second_name,
            Project.title, Project.desc)
    result = await session.execute(statement=stmt)
    projects_info: list[tuple] = result.all()

    projects: list[ProjectData] = []
    for row in projects_info:
        projects.append(ProjectData(
            owner=f"{row[1]} {row[2]}", title=row[3], desc=row[4],
            count_workers=row[5], workers=await get_workrers_info_by_proj(row[0])
        ))

    return AllProjectsData(projects=projects)


async def get_workrers_info_by_proj(
    session: AsyncSession, project_id: int
) -> list[LightWorker]:
    stmt = select(User.id, User.first_name, User.second_name,
        Profession.title, Experience.years
    ).select_from(ProjectWorker).\
    join(User, ProjectWorker.worker_id == User.id).\
    join(Experience, User.id == Experience.user_id).\
    join(Profession, Experience.prof_id == Profession.id).\
    where(ProjectWorker.project_id == project_id)

    result = await session.execute(statement=stmt)
    workers_info: list[tuple] = result.all()
    workers: list[LightWorker] = []
    user_id: Optional[int] = None

    for row in workers_info:
        if user_id is None or user_id != row[0]:
            worker: LightWorker = LightWorker(
                profs=[], fullname=f"{row[1]} {row[2]}"
            )
            workers.append(worker)
            user_id = row[0]
        
        worker.profs.append(ExperianceData(title=row[3], years=row[4]))

    return workers

async def add_project(
    session: AsyncSession, owner_id: int, project_data: ProjectAddData
) -> Optional[int]:
    try:
        project: Project = Project()
        project.desc = project_data.desc
        project.owner_id = owner_id
        project.title = project_data.title
        session.add(project)
    except:
        await session.rollback()
        return None
    else:
        await session.commit()
        await session.refresh(project)
        return project.id
    

async def delete_project(
    session: AsyncSession, project_id: int
) -> bool:
    try:
        project: Project = await session.get(Project, project_id)
        await session.delete(project)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True
    

async def add_worker(
    session: AsyncSession, workers_ids: list[int], project_id: int
) -> bool:
    try:
        for worker_id in workers_ids:
            if not users_dao.is_worker(session=session, user_id=worker_id):
                return False
            project_work: ProjectWorker = ProjectWorker()
            project_work.project_id = project_id
            project_work.worker_id = worker_id
            session.add(project_work)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True