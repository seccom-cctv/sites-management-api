from fastapi import APIRouter, Depends

from services.company import CompanyService
from schemas.company import Company, CompanyBase, CompanyCreate

from config.database import get_db

router = APIRouter(
    prefix="/v1/company",
    tags=["company"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Company)
async def create(company: CompanyCreate, db: get_db = Depends()):
    result = CompanyService(db).create(company)
    return result


@router.get("/{id}", response_model=Company)
async def get(id: int, db: get_db = Depends()):
    result = CompanyService(db).get(id)
    return result