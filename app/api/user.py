from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from typing import Union

from config import settings
from app.schemas.user import (
    UserData,
    UserBase,
    LoginRequest,
    Worker,
    GIP,
    UserDataBase,
)
from app import db_helper
from app.dao import users as user_dao
from app.models.user import User

router: APIRouter = APIRouter(prefix=settings.api.user_prefix)
templates = Jinja2Templates(directory="app/templates")

@router.post("/submit")
async def submit_form(
    user_data: UserData,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        validated_user = await UserData.validate(user_data)
        if user_dao.is_old_user(session=session, email=user_data.email):
            raise HTTPException(status_code=500, detail="Такой пользователь существует")
        user: User = await user_dao.\
                add_user(session=session, user_data=validated_user)
        
        if not user:
            raise HTTPException(status_code=500, detail="Ошибка регистрации")
        
        if user_data.role == "worker":
            if not await  user_dao.add_experianse(
                session=session,
                user_id=user.id,
                prof_id=user_data.profession,
                years=user_data.experience
            ):
                raise HTTPException(status_code=500,
                        detail="Ошибка Добавления стажа")
        
        return JSONResponse(
            content={"message": "Регистрация успешна", "user_id": user.id},
            status_code=200
        )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=UserBase)
async def login(
    login_req: LoginRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserBase:
    user: UserBase = await user_dao.\
            login(session=session, email=login_req.email)
    if not user:
        raise HTTPException(status_code=404,
                        detail="Неизвестный пользователь")
    
    return user


@router.get("/info", response_model=Union[UserDataBase, Worker, GIP])
async def user_info(
    user_id: int = Query(..., alias="id"),
    role: int = Query(..., alias="role"),   
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserData:
    user_info: Union[UserDataBase, Worker, GIP] = \
            await user_dao.get_user_info(session=session,
            user=UserBase(id=user_id, role=role))
    return user_info


@router.get("/workers")
async def user_info(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserData:
    
    return 