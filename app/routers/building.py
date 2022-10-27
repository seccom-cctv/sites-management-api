from fastapi import APIRouter, Depends

from app.services.building import BuildingService
from app.schemas.building import Building, BuildingCreate

from app.utils.service_result import handle_result

from app.config.database import get_db

router = APIRouter(
    prefix="/v1/building",
    tags=["building"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model=Building)
async def get_building(id: int, db: get_db = Depends()):
    result = BuildingService(db).get_building(id)
    return handle_result(result)

@router.post("/", response_model=Building)
async def create_building(building: BuildingCreate, db: get_db = Depends()):
    result = BuildingService(db).create_building(building)
    return handle_result(result)

@router.put("/{id}", response_model=Building)
async def update_building(id: int, building: BuildingCreate, db: get_db = Depends()):
    result = BuildingService(db).update_building(id, building)
    return handle_result(result)

@router.delete("/{id}", response_model=dict)
async def delete_building(id: int, db: get_db = Depends()):
    result = BuildingService(db).delete_building(id)
    return handle_result(result)