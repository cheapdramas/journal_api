from pydantic import BaseModel


class GetSubjectMark(BaseModel):
    student_id:int
    subject: str