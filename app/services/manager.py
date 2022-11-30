from typing import List
from app.schemas.manager import ManagerCreate
from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.models.manager import Manager
from app.utils.service_result import ServiceResult


class ManagerService(AppService):
    def get_manager(self, id: int) -> ServiceResult:
        result = ManagerCRUD(self.db).get_manager(id)
        if not isinstance(result, list):
            return ServiceResult(AppException.Get({"id_not_found": id}))
        #if not result.public:
            # return ServiceResult(AppException.RequiresAuth())
        return ServiceResult(result)

    def create_manager(self, manager: ManagerCreate) -> ServiceResult:
        result = ManagerCRUD(self.db).create_manager(manager)
        if not isinstance(result, Manager):
            return ServiceResult(AppException.Create(result))
        return ServiceResult(result)

    def update_manager(self, id: int, manager: ManagerCreate) -> ServiceResult:
        result = ManagerCRUD(self.db).update_manager(id, manager)
        if not isinstance(result, Manager):
            return ServiceResult(AppException.Update(result))
        return ServiceResult(result)

    def delete_manager(self, id: int) -> ServiceResult:
        result = ManagerCRUD(self.db).delete_manager(id)
        if result == 0:
            return ServiceResult(AppException.Delete({"deleted_rows": result}))
        return ServiceResult({"deleted_rows": result})


class ManagerCRUD(AppCRUD):
    def get_manager(self, id: int) -> List[Manager]:
        if id:
            managers = self.db.query(Manager).filter(Manager.id == id).first()
            managers = [managers] # returns list
        else:
            managers = self.db.query(Manager).all()

        return managers

    def create_manager(self, manager: ManagerCreate) -> Manager:
        manager = Manager(
                    idp_id = manager.idp_id,
                    permissions = manager.permissions,
                    preferences = manager.preferences,
                    company_id = manager.company_id
                    )

        self.db.add(manager)
        self.db.commit()
        self.db.refresh(manager)
        return manager

    def update_manager(self, id: int, manager: ManagerCreate) -> Manager:
        m = self.db.query(Manager).filter(Manager.id == id).one()

        if m:
            m.idp_id = manager.idp_id,
            m.permissions = manager.permissions,
            m.preferences = manager.preferences,
            m.company_id = manager.company_id
            self.db.commit()
            return m

        return None

    def delete_manager(self, id: int) -> int:
        result = self.db.query(Manager).filter(Manager.id == id).delete()
        self.db.commit()
        return result