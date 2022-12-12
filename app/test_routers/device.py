from optparse import Option
from typing import List, Optional
from fastapi import APIRouter, Depends

from app.services.device import DeviceService
from app.schemas.device import Device, DeviceCreate
from app.auth.auth_bearer import JWTBearer
from app.utils.service_result import handle_result
from app.config.database import get_db

router = APIRouter(
    prefix="/v1/device",
    dependencies=[],
    tags=["device"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Device])
async def get_device(id: Optional[int] = None, building_id: Optional[int] = None, db: get_db = Depends()):
    result = DeviceService(db).get_device(id, building_id)
    return handle_result(result)

@router.post("/", response_model=Device)
async def create_device(device: DeviceCreate, db: get_db = Depends()):
    result = DeviceService(db).create_device(device)
    return handle_result(result)

@router.put("/{id}", response_model=Device)
async def update_device(id: int, device: DeviceCreate, db: get_db = Depends()):
    result = DeviceService(db).update_device(id, device)
    return handle_result(result)

@router.delete("/{id}", response_model=dict)
async def delete_device(id: int, db: get_db = Depends()):
    result = DeviceService(db).delete_device(id)
    return handle_result(result)