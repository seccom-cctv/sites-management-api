from typing_extensions import Annotated
from pydantic import BaseModel, Field

class BuildingBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    address: Annotated[str, Field(max_length=255)]
    company_id: int

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int

    class Config:
        orm_mode = True