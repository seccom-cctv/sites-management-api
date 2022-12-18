from typing_extensions import Annotated
from pydantic import BaseModel, Field
from datetime import datetime


class DeviceBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    type: Annotated[str, Field(max_length=255)]
    building_id: int


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
