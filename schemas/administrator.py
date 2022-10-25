from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated

class AdministratorBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    phone: Annotated[str, Field(max_length=30)]
    email: EmailStr
    company_id: int

class AdministratorCreate(AdministratorBase):
    hashed_password: str

class Administrator(AdministratorBase):
    id: int

    class Config:
        orm_mode = True