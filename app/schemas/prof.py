from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from datetime import date

from typing import Optional


class ProfData(BaseModel):
    id: int
    title: str


class ProfsData(BaseModel):
    profs: list[ProfData]


class ExperianceData(BaseModel):
    title: str
    years: int

class ExperiancesData(BaseModel):
    profs: list[ExperianceData]
