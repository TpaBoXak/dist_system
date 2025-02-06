from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

from sqlalchemy import select
from sqlalchemy import func

from typing import Optional

from app.models.project import ProjectWorker, Project


async def get_count_prof_by_u(
    session: AsyncSession,
    user_id: int,
) -> int:
    stmt = select(func.count(Project.id)).where(Project.owner_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()