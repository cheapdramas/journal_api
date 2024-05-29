from fastapi import APIRouter,Form,status,Depends,HTTPException,Request
from fastapi.encoders import jsonable_encoder
from db_scripts import *
import schemas.add_device_schema
import schemas.add_hw_journal_scheme
import schemas.add_mark_journal_scheme
import schemas.add_mark_tg
import schemas.delete_device
import schemas.get_marks_subject
from schemas.get_name_by_id import NameById
from typing import Optional
from fastapi.responses import RedirectResponse
from datetime import date,datetime
import pytz
from config.config import config
from pydantic import BaseModel

import ast
from schemas.device_schema import Check_device,Add_device
from componentCode import get_work_days,get_schedule_day,get_totaldate,all_subjects
import schemas.get_student_id_byname
import schemas.id_teacher_schema
IST = pytz.timezone('Europe/Kiev')
from typing import Annotated
import schemas as schemas
from json import JSONDecoder
from dataclasses import dataclass

@dataclass
class ValueRange:
    min: float
    max: float

router = APIRouter()

@router.post('/{password}/get_names_id/{id}')
async def get_names_by_id_api(id: int):
    return get_names_by_id(id)


    



@router.post('/add_marks_post')
async def send_info_to_db(request:Request):
    print(request.form())
    return RedirectResponse('https://journal-interactive.onrender.com/add_marks',status_code=307)


    # data = await request.body()
    # data = jsonable_encoder(data).split('&')
    # hash_data ={}
    # for i in data:
    #     hash_data[i.split('=')[0]] = i.split('=')[1] 
    
    # print(hash_data)
    
    # date_ = datetime.now(IST).date()
    # time = str(datetime.now(IST)).split(' ')[1].split('.')[0].split(':')[0]+':'+ str(datetime.now(IST)).split(' ')[1].split('.')[0].split(':')[1]
    # subject = all_subjects[int(hash_data['subject'])]
    # if hash_data['reason'] == '':
    #     hash_data['reason'] = None
    # add_mark(int(hash_data['student']),subject,int(hash_data['mark']),hash_data['reason'],date_,time)

    
    


@router.post('/add_marks_journal')
async def add_marks_journal(
    info_mark :schemas.add_mark_journal_scheme.AddMarkScheme
):
    info_mark.student = get_id_by_name(info_mark.student)
    date_ = datetime.now(IST).date()
    time = str(datetime.now(IST)).split(' ')[1].split('.')[0].split(':')[0]+':'+ str(datetime.now(IST)).split(' ')[1].split('.')[0].split(':')[1]
    add_mark(info_mark.student,info_mark.subject,info_mark.mark,info_mark.reason,date=date_,time=time)

@router.post('/add_marks_tg')
async def add_marks_journal(info_mark :schemas.add_mark_tg.AddMarkTg):


    
    date_ = datetime.now(IST).date()
    time = str(datetime.now(IST)).split(' ')[1].split('.')[0].split(':')[0]+':'+ str(datetime.now(IST)).split(' ')[1].split('.')[0].split(':')[1]
    add_mark(info_mark.student_id,info_mark.subject,info_mark.mark,info_mark.reason,date=date_,time=time)


@router.post('/get_student_id_by_name_scname')
async def get_student_id_by_name_url(name:schemas.get_student_id_byname.GetStudentIdByName) ->int:
    id_student = get_id_by_name(name.name)

    return id_student
    
@router.post('/schedule_day')
async def schedule_day(option=Form()):
    print(get_schedule_day(option))

    return get_schedule_day(option)





@router.post('/add_homework_done')
async def homework_done(
    request:Request
    ):
    data = await request.body()
    data = ast.literal_eval(jsonable_encoder(data))['data']
    
    
    subj_index = int(data['subject'])
    if data['hw'] == '':
        data['hw']= None

    is_there_hw(total_date=get_totaldate(data['date']),subj=get_schedule_day(data['date'])[subj_index-1]['text'],subj_index=subj_index,desc=data['hw'])
    




@router.post('/add_homework_journal')
async def homework_done_journal(
    hw: schemas.add_hw_journal_scheme.AddHwJournalScheme):
    total_date = get_totaldate(hw.date)

    
    subject_index = hw.subject
    
    #index_subj = [i['text'] ==hw.subject for i in get_schedule_day(int(hw.date))].index(True) +1
    found = False
    for i in get_schedule_day(hw.date):
        if i['text'] == hw.subject:
            found = True
            is_there_hw(total_date,hw.subject,i['index'],hw.homework)
    if not found:
        raise HTTPException(status_code=404,detail={'error':"not found"})
    
    
    

    # except Exception as exception:
    #     print('asd')

   

    
    
    


@router.post('/check_device')
async def check_device_url(device: Check_device):
    a = devices_id('CHECK',device.device)
    try:
        if bool(a[1]):
            a = (a[0],a[1],get_teacher_privelege(a[0]))
    except:
        print(a)
    return a

@router.post('/{password}/add_device')
async def add_device_url(password:str,device:schemas.add_device_schema.AddDeviceScheme):
    if password == config['password']:
        devices_id('ADD',device.device_id,device.log_id,device.is_teacher)







@router.post('/teacher_name')
async def get_teacher_name_url(password:str,id:schemas.id_teacher_schema.IdScheme):
    if password == config['password']:
        return get_teacher_name_by_id(id.id)



@router.post('/student_subject_marks')
async def student_subject_mark(password:str,scheme: schemas.get_marks_subject.GetSubjectMark):
    student_id = scheme.student_id
    subject= scheme.subject

    return get_subject_marks(student_id,subject)


@router.post('/delete_acc')
async def delete_device_url(password:str,scheme:schemas.delete_device.DeleteDevice):
    if password == config['password']:
        delete_device(scheme.device_id)




@router.post('/change_schedule')
async def change_schedule_monday_url(day_index:Annotated[int,ValueRange(1,5)],request:Request):
    data = await request.body()
    data = jsonable_encoder(data)
    
    data =ast.literal_eval(data)['subjects']
    for i in data:
        if i==0:
            data[data.index(i)] = None
    print(data)
    change_schedule(day_index,data)






    
