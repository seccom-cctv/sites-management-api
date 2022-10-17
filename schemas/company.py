from typing import Optional, Any, Union
from pydantic import BaseModel, EmailStr
from administrator import Administrator
from building import Building

class CompanyBase(BaseModel):
    name: str
    address: str
    phone: str
    email: Optional[EmailStr]

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    buildings: list[Building]
    administrators: list[Administrator]

    class Config:
        orm_mode = True