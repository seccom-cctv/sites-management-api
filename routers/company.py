from fastapi import APIRouter, Depends

from services.company import CompanyService
from schemas.company import *

from config.database import get_db

router = APIRouter(
    prefix="/v1/company",
    tags=["company"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Company)
async def create_item(item: CompanyCreate, db: get_db = Depends()):
    result = CompanyService(db).create(item)
    return result


@router.get("/{item_id}", response_model=Company)
async def get_item(item_id: int, db: get_db = Depends()):
    result = CompanyService(db).get(item_id)
    return result