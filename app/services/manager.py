from typing import List
from schemas.manager import ManagerCreate
from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from models.manager import Manager
from utils.service_result import ServiceResult

import config.settings as settings
from utils.aux_functions import is_admin, is_manager

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
        manager_idp_id =  settings.request_payload["sub"]
        manager = self.db.query(Manager).filter(Manager.idp_id == manager_idp_id).first()

        if not (manager.id == id or is_admin()):
            return None

        if id:
            managers = [manager] # returns list
        elif is_admin():
            managers = self.db.query(Manager).all()

        return managers

    def create_manager(self, manager: ManagerCreate) -> Manager:
        if not is_admin():
            return None

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
        manager_idp_id =  settings.request_payload["sub"]
        request_manager = self.db.query(Manager).filter(Manager.idp_id == manager_idp_id).first()

        if is_admin():
            pass
        else:
            '''If manager is not admin Only allows him to update the preferences. Every other attribute remains the same'''
            request_manager.preferences = manager.preferences
            id = request_manager.id
            manager = request_manager

        m = self.db.query(Manager).filter(Manager.id == id).one()

        if m:
            m.idp_id = manager.idp_id,
            m.permissions = manager.permissions,
            m.preferences = manager.preferences,
            m.company_id = manager.company_id
            self.db.commit()
            self.db.refresh(manager)
            return m

        return None

    def delete_manager(self, id: int) -> int:
        if not is_admin():
            return None

        result = self.db.query(Manager).filter(Manager.id == id).delete()
        self.db.commit()
        return result