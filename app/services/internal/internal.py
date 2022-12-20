import sqlalchemy
from typing import List
from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from utils.service_result import ServiceResult

from models.building import Building
from models.manager import Manager
from models.device import Device
from models.company import Company

from sqlalchemy.orm import joinedload
from ..main import get_cognito_user_pool

class InternalService(AppService):
    def get_device_managers(self, device_id: int) -> ServiceResult:
        result = InternalCRUD(self.db).get_device_managers(device_id)
        if not isinstance(result, list):
            return ServiceResult(AppException.Get({"id_not_found": device_id}))

        return ServiceResult(result)

class InternalCRUD(AppCRUD):
    def get_device_managers(self, device_id: int) -> List:
        try:
            # Get the company for the device's building
            company = self.db.query(Company).join(Company.buildings).join(Building.devices).filter(Device.id==device_id).options(joinedload(Company.managers)).one()

            # Get the managers for the company
            managers = company.managers
            wanted_idp_ids = {manager.idp_id for manager in managers}

            users = get_cognito_user_pool()
            device_managers = []
            for user in users:
                if user["Username"] in wanted_idp_ids:
                    device_managers.append(user)

        except sqlalchemy.exc.NoResultFound as e:
            print("ERROR:", e)
            return None

        return device_managers