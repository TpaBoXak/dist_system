from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import settings
from app.schemas.user import UserData

router: APIRouter = APIRouter(prefix=settings.api.user_prefix)
templates = Jinja2Templates(directory="app/templates")

@router.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    user_data: UserData
):
    return templates.TemplateResponse(
        "result.html", 
        {
            "request": request, 
            "name": user_data.name,
            "surname": user_data.surname,
            "phone": user_data.phone,
            "birth_date": user_data.birth_date,
            "email": user_data.email,
            "profession": user_data.profession,
            "experience": user_data.experience
        }
    )