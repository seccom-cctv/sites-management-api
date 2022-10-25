from schemas.administrator import AdministratorCreate
from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from models.administrator import Administrator
from utils.service_result import ServiceResult


class AdministratorService(AppService):
    def get_administrator(self, id: int) -> ServiceResult:
        administrator = AdministratorCRUD(self.db).get_administrator(id)
        if not administrator:
            return ServiceResult(AppException.Get({"id": id}))
        #if not administrator.public:
            # return ServiceResult(AppException.RequiresAuth())
        return ServiceResult(administrator)

    def create_administrator(self, administrator: AdministratorCreate) -> ServiceResult:
        administrator = AdministratorCRUD(self.db).create_administrator(administrator)
        if not administrator:
            return ServiceResult(AppException.Create())
        return ServiceResult(administrator)

    def update_administrator(self, id: int, administrator: AdministratorCreate) -> ServiceResult:
        administrator = AdministratorCRUD(self.db).update_administrator(id, administrator)
        if not administrator:
            return ServiceResult(AppException.Update())
        return ServiceResult(administrator)

    def delete_administrator(self, id: int) -> ServiceResult:
        result = AdministratorCRUD(self.db).delete_administrator(id)
        if result == 0:
            return ServiceResult(AppException.Delete({"deleted_rows": result}))
        return ServiceResult({"deleted_rows": result})


class AdministratorCRUD(AppCRUD):
    def get_administrator(self, id: int) -> Administrator:
        administrator = self.db.query(Administrator).filter(Administrator.id == id).first()

        if administrator:
            return administrator

        return None

    def create_administrator(self, administrator: AdministratorCreate) -> Administrator:
        administrator = Administrator(
                    name = administrator.name,
                    phone = administrator.phone,
                    email = administrator.email,
                    hashed_password = administrator.hashed_password,
                    company_id = administrator.company_id
                    )

        self.db.add(administrator)
        self.db.commit()
        self.db.refresh(administrator)
        return administrator

    def update_administrator(self, id: int, administrator: AdministratorCreate) -> Administrator:
        a = self.db.query(Administrator).filter(Administrator.id == id).one()

        if a:
            a.name = administrator.name,
            a.phone = administrator.phone,
            a.email = administrator.email
            a.hashed_password = administrator.hashed_password
            a.company_id = administrator.company_id
            self.db.commit()
            return a

        return None

    def delete_administrator(self, id: int) -> int:
        result = self.db.query(Administrator).filter(Administrator.id == id).delete()
        self.db.commit()
        return result