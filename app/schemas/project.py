from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from datetime import date

from typing import Optional

from app.schemas.user import LightWorker


class ProjectAddData(BaseModel):
    title: str
    desc: str
    workers: list[int]


class ProjectData(BaseModel):
    owner: str
    title: str
    desc: str
    count_workers: int
    workers: list[Optional[LightWorker]]

class AllProjectsData(BaseModel):
    projects: list[Optional[ProjectData]]