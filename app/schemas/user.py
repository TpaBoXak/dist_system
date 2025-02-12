from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from datetime import date

from typing import Optional

from app.schemas.prof import ExperiancesData


class UserDataBase(BaseModel):
    name: str
    surname: str
    phone: str
    birth_date: date
    email: EmailStr
    role: int


class UserNameId(BaseModel):
    id: int
    name: str

class Worker(UserDataBase, ExperiancesData):
    pass

class LightWorker(ExperiancesData):
    fullname: str


class Workers(BaseModel):
    workers: list[Worker]

class GIP(UserDataBase):
    count_proj: int = Field(ge=0)

class UserData(BaseModel):
    name: str
    surname: str
    phone: str
    birth_date: date
    email: EmailStr
    role: str

    profession: Optional[int] = None
    experience: Optional[int] = Field(default=None, ge=0)

    @classmethod
    async def validate(cls, data):
        if data.role == "worker":
            if not data.profession:
                raise ValueError("Профессия обязательна для работника")
            if data.experience is None:
                raise ValueError("Стаж работы обязателен для работника")
        else:
            data.profession= None
            data.experience = None
        return data
    
class UserBase(BaseModel):
    id: int
    role: int


class LoginRequest(BaseModel):
    email: str
