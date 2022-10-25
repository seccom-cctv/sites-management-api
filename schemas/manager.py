from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated

class ManagerBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    phone: Annotated[str, Field(max_length=30)]
    email: EmailStr
    company_id: int

class ManagerCreate(ManagerBase):
    hashed_password: str

class Manager(ManagerBase):
    id: int

    class Config:
        orm_mode = True