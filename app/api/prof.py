from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import ValidationError

from config import settings
from app import db_helper
from app.dao import prof as prof_dao
from app.models.profession import Profession
from app.schemas.prof import ProfData, ProfsData

router: APIRouter = APIRouter(prefix=settings.api.prof_prefix)
templates = Jinja2Templates(directory="app/templates")

@router.get("/all", response_model=ProfsData)
async def submit_form(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    profs: list[ProfData] = await prof_dao.get_all_prof(session=session)
    profs_data: ProfsData = ProfsData(profs= [prof for prof in profs])
    return profs_data