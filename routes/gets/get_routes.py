from fastapi import APIRouter,Request,Form,Depends,HTTPException
from fastapi.responses import RedirectResponse
from http_basic import HTTPBasicCredentials,HTTPBasic
from fastapi.templating import Jinja2Templates
from db_scripts import get_log_pass,get_id_name_second_name,get_marks,get_news_by_id,get_homework,get_schedule
from pathlib import Path
from componentCode import homework_days_represent,all_subjects
from pydantic import BaseModel
from starlette_context import context,middleware,plugins
from typing import Annotated
from config.config import config
from dataclasses import dataclass

@dataclass
class ValueRange:
    min: float
    max: float


router = APIRouter()
PATH = Path(__file__).parent.parent.parent
print(PATH)
templates = Jinja2Templates(directory=f'{PATH}/templates')


security = HTTPBasic()


@router.get('/')
async def lobby(request:Request):
    
    return templates.TemplateResponse('this_is_just_api.html',{'request':request})


@router.get('/get_schedule')
async def get_schedule_day_post(day_index:Annotated[int,ValueRange(0,4)]):
    schedule = get_schedule()[day_index][1:]
    schedule = [i for i in schedule]
    for i in schedule:
        if i == None:
            schedule[schedule.index(i)] = ''

    return schedule





@router.get('/get_dates_represent')
async def get_dates_represent_url():

    return homework_days_represent()
