from schemas.building import BuildingCreate
from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from models.building import Building
from utils.service_result import ServiceResult


class BuildingService(AppService):
    def get_building(self, id: int) -> ServiceResult:
        building = BuildingCRUD(self.db).get_building(id)
        if not building:
            return ServiceResult(AppException.Get({"id": id}))
        #if not building.public:
            # return ServiceResult(AppException.RequiresAuth())
        return ServiceResult(building)

    def create_building(self, building: BuildingCreate) -> ServiceResult:
        building = BuildingCRUD(self.db).create_building(building)
        if not building:
            return ServiceResult(AppException.Create())
        return ServiceResult(building)

    def update_building(self, id: int, building: BuildingCreate) -> ServiceResult:
        building = BuildingCRUD(self.db).update_building(id, building)
        if not building:
            return ServiceResult(AppException.Update())
        return ServiceResult(building)

    def delete_building(self, id: int) -> ServiceResult:
        result = BuildingCRUD(self.db).delete_building(id)
        if result == 0:
            return ServiceResult(AppException.Delete({"deleted_rows": result}))
        return ServiceResult({"deleted_rows": result})


class BuildingCRUD(AppCRUD):
    def get_building(self, id: int) -> Building:
        building = self.db.query(Building).filter(Building.id == id).first()

        if building:
            return building

        return None

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
            b.name = building.name,
            b.address = building.address,
            b.company_id = building.company_id,
            self.db.commit()
            return b

        return None

    def delete_building(self, id: int) -> int:
        result = self.db.query(Building).filter(Building.id == id).delete()
        self.db.commit()
        return result