from typing import List, Optional
from fastapi import APIRouter, Depends

from services.manager import ManagerService
from schemas.manager import Manager, ManagerCreate
from auth.auth_bearer import JWTBearer
from utils.service_result import handle_result
from config.database import get_db

router = APIRouter(
    prefix="/v1/manager",
    dependencies=[Depends(JWTBearer())],
    tags=["manager"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Manager])
async def get_manager(id: Optional[int] = None, db: get_db = Depends()):
    result = ManagerService(db).get_manager(id)
    return handle_result(result)

@router.post("/", response_model=Manager)
async def create_manager(manager: ManagerCreate, db: get_db = Depends()):
    result = ManagerService(db).create_manager(manager)
    return handle_result(result)

@router.put("/", response_model=Manager)
async def update_manager(manager: ManagerCreate, id: Optional[int] = None, db: get_db = Depends()):
    result = ManagerService(db).update_manager(id, manager)
    return handle_result(result)

@router.delete("/{id}", response_model=dict)
async def delete_manager(id: int, db: get_db = Depends()):
    result = ManagerService(db).delete_manager(id)
    return handle_result(result)