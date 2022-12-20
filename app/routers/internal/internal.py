from typing import List
from schemas.manager import Manager
from fastapi import APIRouter, Depends

from services.internal.internal import InternalService
from utils.service_result import handle_result
from config.database import get_db

router = APIRouter(
    prefix="/v1/internal",
    tags=["internal"],
    responses={404: {"description": "Not found"}},
)

@router.get("/device_managers/{device_id}", response_model=List[Manager])
async def get_device_managers(device_id: int, db: get_db = Depends()):
    result = InternalService(db).get_device_managers(device_id)
    return handle_result(result)