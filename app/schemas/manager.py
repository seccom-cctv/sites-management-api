from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from typing_extensions import Annotated

class ManagerBase(BaseModel):
    idp_id: str
    preferences: Optional[str]
    permissions: Optional[int]
    company_id: int

class ManagerCreate(ManagerBase):
    pass

class Manager(ManagerBase):
    id: int

    class Config:
        orm_mode = True