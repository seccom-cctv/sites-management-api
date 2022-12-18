from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field
from schemas.manager import Manager
from schemas.building import Building

class CompanyBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    address: Annotated[str, Field(max_length=255)]
    phone: Annotated[str, Field(max_length=30)]
    email: Optional[EmailStr]

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    managers: list[Manager]
    buildings: list[Building]

    class Config:
        orm_mode = True