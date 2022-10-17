from typing import Optional, Any, Union
from pydantic import BaseModel, EmailStr
from company import Company

class AdministratorBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    company_id: int
    company: Company

class AdministratorCreate(AdministratorBase):
    password: str

class Administrator(AdministratorBase):
    id: int

    class Config:
        orm_mode = True