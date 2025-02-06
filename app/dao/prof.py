from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

from sqlalchemy import select

from typing import Optional

from app.schemas.prof import ProfData, ExperianceData, ExperiancesData
from app.models.profession import Profession, Experience


async def get_all_prof(
    session: AsyncSession,
) -> list[ProfData]:
    stmt = select(Profession.id, Profession.title)
    result = await session.execute(stmt)
    all_profs_bd: list[Profession] = result.all()
    all_profs: list[ProfData] = []
    for prof in all_profs_bd:
        all_profs.append(
            ProfData(
                id=prof[0],
                title=prof[1]
            )
        )
    
    return all_profs


async def get_exp_by_user_id(
    session: AsyncSession,
    user_id: int
) -> ExperiancesData:
    stmt = select(Profession.title, Experience.years).\
        select_from(Experience).\
        join(Profession, Experience.prof_id == Profession.id).\
        where(Experience.user_id == user_id)
    result = await session.execute(statement=stmt)
    exp_info: list[tuple] = result.all()
    profs: list[ExperianceData] = []
    for row in exp_info:
        profs.append(ExperianceData(
            title=row[0],
            years=row[1]
        ))
    
    return ExperiancesData(profs=profs)