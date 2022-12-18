from typing import List
from models.manager import Manager
from schemas.device import DeviceCreate
from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from models.device import Device
from utils.service_result import ServiceResult

import config.settings as settings
from utils.aux_functions import is_admin, is_manager


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

            if not (is_manager(devices[0].building_id) or is_admin()):
                return None

        elif building_id and (is_manager(building_id) or is_admin()):
            devices = self.db.query(Device).filter(Device.building_id == building_id).all()
        elif is_admin():
            devices = self.db.query(Device).all()
        else:
            return None

        return devices

    def create_device(self, device: DeviceCreate) -> Device:
        if not (is_manager(device.building_id) or is_admin()):
            return None

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
        query_device = self.db.query(Device).filter(Device.id == id).first()

        if not ((is_manager(query_device.building_id) and is_manager(device.building_id)) or is_admin()):
            return None

        d = self.db.query(Device).filter(Device.id == id).one()

        if d:
            d.name = device.name,
            d.type = device.type,
            d.building_id = device.building_id
            self.db.commit()
            return d

        return None

    def delete_device(self, id: int) -> int:
        device = self.db.query(Device).filter(Device.id == id).first()

        if not (is_manager(device.building_id) or is_admin()):
            return None

        self.db.query(Device).filter(Device.id == id).delete()
        self.db.commit()
        return device

    def get_building_devices(self, building_id) -> List[Device]:
        manager_idp_id =  settings.request_payload["sub"]
        manager = self.db.query(Manager).filter(Manager.idp_id == manager_idp_id).first()
        building = list(filter(lambda b: b.id == building_id, manager.company.buildings))
        is_manager_of_building = True if len(building) else False
        
        if is_manager_of_building:
            devices = self.db.query(Device).filter(Device.building_id == building_id).all()
            return devices
        
        return None