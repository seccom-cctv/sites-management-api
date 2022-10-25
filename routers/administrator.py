from fastapi import APIRouter, Depends

from services.administrator import AdministratorService
from schemas.administrator import Administrator, AdministratorCreate

from utils.service_result import handle_result

from config.database import get_db

router = APIRouter(
    prefix="/v1/administrator",
    tags=["administrator"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model=Administrator)
async def get_administrator(id: int, db: get_db = Depends()):
    result = AdministratorService(db).get_administrator(id)
    return handle_result(result)

@router.post("/", response_model=Administrator)
async def create_administrator(administrator: AdministratorCreate, db: get_db = Depends()):
    result = AdministratorService(db).create_administrator(administrator)
    return handle_result(result)

@router.put("/{id}", response_model=Administrator)
async def update_administrator(id: int, administrator: AdministratorCreate, db: get_db = Depends()):
    result = AdministratorService(db).update_administrator(id, administrator)
    return handle_result(result)

@router.delete("/{id}", response_model=dict)
async def delete_administrator(id: int, db: get_db = Depends()):
    result = AdministratorService(db).delete_administrator(id)
    return handle_result(result)