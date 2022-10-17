from typing import Optional, Any, Union
from pydantic import BaseModel, EmailStr
from models.models import Company, Device

class BuildingBase(BaseModel):
    name: str
    address: str
    company_id: int
    company: Company

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int
    devices: list[Device]

    class Config:
        orm_mode = True