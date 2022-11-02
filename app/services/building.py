from typing import List
from app.schemas.building import BuildingCreate
from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.models.building import Building
from app.utils.service_result import ServiceResult


class BuildingService(AppService):
    def get_building(self, id: int, company_id: int) -> ServiceResult:
        result = BuildingCRUD(self.db).get_building(id, company_id)
        if not isinstance(result, list):
            return ServiceResult(AppException.Get({"id_not_found": id}))
        #if not result.public:
            # return ServiceResult(AppException.RequiresAuth())
        return ServiceResult(result)

    def create_building(self, building: BuildingCreate) -> ServiceResult:
        result = BuildingCRUD(self.db).create_building(building)
        if not isinstance(result, Building):
            return ServiceResult(AppException.Create(result))
        return ServiceResult(result)

    def update_building(self, id: int, building: BuildingCreate) -> ServiceResult:
        result = BuildingCRUD(self.db).update_building(id, building)
        if not isinstance(result, Building):
            return ServiceResult(AppException.Update(result))
        return ServiceResult(result)

    def delete_building(self, id: int) -> ServiceResult:
        result = BuildingCRUD(self.db).delete_building(id)
        if result == 0:
            return ServiceResult(AppException.Delete({"deleted_rows": result}))
        return ServiceResult({"deleted_rows": result})


class BuildingCRUD(AppCRUD):
    def get_building(self, id: int, company_id: int) -> List[Building]:
        if id:
            buildings = self.db.query(Building).filter(Building.id == id).first()
            buildings = [buildings] # returns list
        elif company_id:
            buildings = self.db.query(Building).filter(Building.company_id == company_id).all()
        else:
            buildings = self.db.query(Building).all()

        return buildings

    def create_building(self, building: BuildingCreate) -> Building:
        building = Building(
                    name = building.name,
                    address = building.address,
                    company_id = building.company_id,
                    )

        self.db.add(building)
        self.db.commit()
        self.db.refresh(building)
        return building

    def update_building(self, id: int, building: BuildingCreate) -> Building:
        b = self.db.query(Building).filter(Building.id == id).one()

        if b:
            b.name = building.name
            b.address = building.address
            b.company_id = building.company_id
            self.db.commit()
            return b

        return None

    def delete_building(self, id: int) -> int:
        result = self.db.query(Building).filter(Building.id == id).delete()
        self.db.commit()
        return result