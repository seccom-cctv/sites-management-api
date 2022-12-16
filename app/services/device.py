from typing import List
from app.config.database import session
from app.models.building import Building
from app.models.manager import Manager
from app.schemas.device import DeviceCreate
from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.models.device import Device
from app.utils.service_result import ServiceResult

import app.config.settings as settings


class DeviceService(AppService):
    def get_device(self, id: int, building_id: int) -> ServiceResult:
        result = DeviceCRUD(self.db).get_device(id, building_id)
        if not isinstance(result, list):
            return ServiceResult(AppException.Get({"id_not_found": id}))

        return ServiceResult(result)

    def create_device(self, device: DeviceCreate) -> ServiceResult:
        result = DeviceCRUD(self.db).create_device(device)
        if not isinstance(result, Device):
            return ServiceResult(AppException.Create(result))
        return ServiceResult(result)

    def update_device(self, id: int, device: DeviceCreate) -> ServiceResult:
        result = DeviceCRUD(self.db).update_device(id, device)
        if not isinstance(result, Device):
            return ServiceResult(AppException.Update(result))
        return ServiceResult(result)

    def delete_device(self, id: int) -> ServiceResult:
        result = DeviceCRUD(self.db).delete_device(id)
        if result == 0:
            return ServiceResult(AppException.Delete({"deleted_rows": result}))
        return ServiceResult({"deleted_rows": result})

    def get_building_devices(self, building_id: int) -> ServiceResult:
        result = DeviceCRUD(self.db).get_building_devices(building_id)
        if not isinstance(result, list):
            return ServiceResult(AppException.Get({"error": f"Permission denied for building_id '{building_id}' or invalid building_id"}))

        return ServiceResult(result)


class DeviceCRUD(AppCRUD):
    def get_device(self, id: int, building_id: int) -> List[Device]:
        if id:
            devices = self.db.query(Device).filter(Device.id == id).first()
            devices = [devices] # returns list
        elif building_id:
            devices = self.db.query(Device).filter(Device.building_id == building_id).all()
        else:
            devices = self.db.query(Device).all()

        return devices

    def create_device(self, device: DeviceCreate) -> Device:
        device = Device(
                    name = device.name,
                    type = device.type,
                    building_id = device.building_id
                    )

        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def update_device(self, id: int, device: DeviceCreate) -> Device:
        d = self.db.query(Device).filter(Device.id == id).one()

        if d:
            d.name = device.name,
            d.type = device.type,
            d.building_id = device.building_id
            self.db.commit()
            return d

        return None

    def delete_device(self, id: int) -> int:
        result = self.db.query(Device).filter(Device.id == id).delete()
        self.db.commit()
        return result

    def get_building_devices(self, building_id) -> List[Device]:
        manager_idp_id =  settings.request_payload["sub"]
        manager = session.query(Manager).filter(Manager.idp_id == manager_idp_id).first()
        building = list(filter(lambda b: b.id == building_id, manager.company.buildings))
        is_manager_of_building = True if len(building) else False
        
        if is_manager_of_building:
            devices = session.query(Device).filter(Device.building_id == building_id).all()
            return devices
        
        return None