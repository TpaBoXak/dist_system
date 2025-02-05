from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from datetime import date


class UserData(BaseModel):
    name: str
    surname: str
    phone: str
    birth_date: date
    email: EmailStr
    profession: str
    experience: int = Field(ge=0)