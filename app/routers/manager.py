from typing import List, Optional
from fastapi import APIRouter, Depends

from app.services.manager import ManagerService
from app.schemas.manager import Manager, ManagerCreate
from app.auth.auth_bearer import JWTBearer
from app.utils.service_result import handle_result
from app.config.database import get_db

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

@router.put("/{id}", response_model=Manager)
async def update_manager(id: int, manager: ManagerCreate, db: get_db = Depends()):
    result = ManagerService(db).update_manager(id, manager)
    return handle_result(result)

@router.delete("/{id}", response_model=dict)
async def delete_manager(id: int, db: get_db = Depends()):
    result = ManagerService(db).delete_manager(id)
    return handle_result(result)