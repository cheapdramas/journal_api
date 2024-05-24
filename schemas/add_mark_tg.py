from pydantic import BaseModel


class AddMarkTg(BaseModel):
    student_id:int
    subject: str
    mark: int
    reason:str