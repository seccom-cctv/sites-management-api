from fastapi import APIRouter, Depends

from app.services.company import CompanyService
from app.schemas.company import Company, CompanyCreate

from app.utils.service_result import handle_result

from app.config.database import get_db

router = APIRouter(
    prefix="/v1/company",
    tags=["company"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model=Company)
async def get_company(id: int, db: get_db = Depends()):
    result = CompanyService(db).get_company(id)
    return handle_result(result)

@router.post("/", response_model=Company)
async def create_company(company: CompanyCreate, db: get_db = Depends()):
    result = CompanyService(db).create_company(company)
    return handle_result(result)

@router.put("/{id}", response_model=Company)
async def update_company(id: int, company: CompanyCreate, db: get_db = Depends()):
    result = CompanyService(db).update_company(id, company)
    return handle_result(result)

@router.delete("/{id}", response_model=dict)
async def delete_company(id: int, db: get_db = Depends()):
    result = CompanyService(db).delete_company(id)
    return handle_result(result)