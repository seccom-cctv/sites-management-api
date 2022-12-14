from typing import Optional, List
from fastapi import APIRouter, Depends

from services.building import BuildingService
from schemas.building import Building, BuildingCreate
from auth.auth_bearer import JWTBearer
from utils.service_result import handle_result
from config.database import get_db

router = APIRouter(
    prefix="/v1/building",
    dependencies=[Depends(JWTBearer())],
    tags=["building"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Building])
async def get_building(id: Optional[int] = None, company_id: Optional[int] = None, db: get_db = Depends()):
    result = BuildingService(db).get_building(id, company_id)
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

@router.get("/manager_buildings", response_model=List[Building])
async def get_manager_building(db: get_db = Depends()):
    result = BuildingService(db).get_manager_buildings()
    return handle_result(result)