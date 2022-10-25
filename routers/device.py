from fastapi import APIRouter, Depends

from services.device import DeviceService
from schemas.device import Device, DeviceCreate

from utils.service_result import handle_result

from config.database import get_db

router = APIRouter(
    prefix="/v1/device",
    tags=["device"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model=Device)
async def get_device(id: int, db: get_db = Depends()):
    result = DeviceService(db).get_device(id)
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