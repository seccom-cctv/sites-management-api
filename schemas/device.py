from typing import Optional, Any, Union
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field

class DeviceBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    type: Annotated[str, Field(max_length=255)]
    building_id: int

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True