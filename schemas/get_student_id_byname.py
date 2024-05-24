from pydantic import BaseModel

class GetStudentIdByName(BaseModel):
    name: str