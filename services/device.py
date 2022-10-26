from schemas.device import DeviceCreate
from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from models.device import Device
from utils.service_result import ServiceResult


class DeviceService(AppService):
    def get_device(self, id: int) -> ServiceResult:
        result = DeviceCRUD(self.db).get_device(id)
        if not isinstance(result, Device):
            return ServiceResult(AppException.Get(result))
        #if not result.public:
            # return ServiceResult(AppException.RequiresAuth())
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


class DeviceCRUD(AppCRUD):
    def get_device(self, id: int) -> Device:
        device = self.db.query(Device).filter(Device.id == id).first()

        if device:
            return device

        return None

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