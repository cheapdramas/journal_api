from pydantic import BaseModel


class DeleteDevice(BaseModel):
    device_id: str