from typing import Optional, Any, Union
from pydantic import BaseModel, EmailStr
from models.models import Administrator, Building

class CompanyBase(BaseModel):
    name: str
    address: str
    phone: str
    email: Optional[EmailStr]

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    buildings: list[Any]
    administrators: list[Any]

    class Config:
        orm_mode = True