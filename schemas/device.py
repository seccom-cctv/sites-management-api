from typing import Optional, Any, Union
from pydantic import BaseModel, EmailStr
from models.models import Building

class DeviceBase(BaseModel):
    name: str
    type: str
    building_id: int
    building: Building

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True