from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

from sqlalchemy import select
from sqlalchemy import func

from typing import Optional

from app.dao import prof as prof_dao
from app.schemas.user import (
    UserData, UserBase, UserDataBase, Worker, GIP, UserNameId
)
from app.schemas.prof import ExperiancesData, ExperianceData
from app.models.user import User, UserRole
from app.models.profession import Experience
from app.models.project import Project


async def add_user(
    session: AsyncSession,
    user_data: UserData
) -> Optional[User]:
    try:
        user: User = User()
        user.first_name = user_data.name
        user.second_name = user_data.surname
        user.email = user_data.email
        user.phone = user_data.phone
        user.birthday = user_data.birth_date
        user.role_id = 2 if user_data.role == "worker" else 3
        session.add(user)
    except:
        await session.rollback()
        return None
    else:
        await session.commit()
        await session.refresh(user)
        return user
        

async def add_experianse(
    session: AsyncSession,
    user_id: int,
    prof_id: int,
    years: int,
) -> bool:
    try:
        exp: Experience = Experience()
        exp.prof_id = prof_id
        exp.user_id = user_id
        exp.years = years
        session.add(exp)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True
    

async def login(
    session: AsyncSession,
    email: str
) -> Optional[UserBase]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(statement=stmt)
    user: User = result.scalar_one_or_none()
    if not user: return None
    return UserBase(id=user.id, role=user.role_id)


async def get_count_proj_by_u(
    session: AsyncSession,
    user_id: int,
) -> int:
    stmt = select(func.count(Project.id)).where(Project.owner_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_info(
    session: AsyncSession,
    user: UserBase
) -> UserData:
    user_bd: User = await session.get(User, user.id)
    if not user_bd:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info = UserDataBase(
        name=user_bd.first_name,
        surname=user_bd.second_name,
        birth_date=user_bd.birthday,
        phone=user_bd.phone,
        email=user_bd.email,
        role=user_bd.role_id
    )

    if user_bd.role_id == 2:
        exp_data: ExperiancesData = await prof_dao.\
                get_exp_by_user_id(session=session, user_id=user.id)
        worker_data = {**user_info.model_dump(), **exp_data.model_dump()}
        user_info: Worker = Worker(**worker_data)

    elif user_bd.role_id == 3:
        project_count = await get_count_proj_by_u(session=session, user_id=user.id)
        user_info: GIP = GIP(**user_info.model_dump(),
                count_proj=project_count)

    return user_info


async def is_old_user(
    session: AsyncSession,
    email: str
) -> Optional[UserBase]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(statement=stmt)
    user: User = result.scalar_one_or_none()
    if user: return True
    return False


async def is_gip(
    session: AsyncSession,
    user_id: int
) -> bool:
    user: User = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role_id == 3:
        return True
    return False


async def is_worker(
    session: AsyncSession,
    user_id: int
) -> bool:
    user: User = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role_id == 2:
        return True
    return False


async def get_workers(
    session: AsyncSession
) -> list[UserNameId]:
    stmt = select(User.id, User.second_name, User.first_name).\
        where(User.role_id == 2)
    result = await session.execute(statement=stmt)
    users_info: list[tuple] = result.all()
    users: list[UserNameId] = []
    for row in users_info:
        users.append(
            UserNameId(id=row[0], name=f"{row[1]} {row[2]}")
        )

    return users


async def get_gips(
    session: AsyncSession
) -> list[GIP]:
    stmt = select(
        User.second_name, User.first_name, User.phone,
        User.birthday, User.email, User.role_id, User.id
    ).where(User.role_id == 3)
    result = await session.execute(statement=stmt)
    gips_info: list[tuple] = result.all()
    gips: list[GIP] = []
    for row in gips_info:
        gips.append(GIP(
            surname=row[0],
            name=row[1],
            phone=row[2],
            birth_date=row[3],
            email=row[4],
            role=row[5],
            count_proj= await get_count_proj_by_u(
                session=session,
                user_id=row[6]
            )
        ))

    return gips