from schemas.company import CompanyCreate
from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from models.company import Company
from utils.service_result import ServiceResult


class CompanyService(AppService):
    def get_company(self, id: int) -> ServiceResult:
        company = CompanyCRUD(self.db).get_company(id)
        if not company:
            return ServiceResult(AppException.Get({"id": id}))
        #if not company.public:
            # return ServiceResult(AppException.RequiresAuth())
        return ServiceResult(company)

    def create_company(self, company: CompanyCreate) -> ServiceResult:
        company = CompanyCRUD(self.db).create_company(company)
        if not company:
            return ServiceResult(AppException.Create())
        return ServiceResult(company)

    def update_company(self, id: int, company: CompanyCreate) -> ServiceResult:
        company = CompanyCRUD(self.db).update_company(id, company)
        if not company:
            return ServiceResult(AppException.Update())
        return ServiceResult(company)

    def delete_company(self, id: int) -> ServiceResult:
        result = CompanyCRUD(self.db).delete_company(id)
        if result == 0:
            return ServiceResult(AppException.Delete({"deleted_rows": result}))
        return ServiceResult({"deleted_rows": result})


class CompanyCRUD(AppCRUD):
    def get_company(self, id: int) -> Company:
        company = self.db.query(Company).filter(Company.id == id).first()

        if company:
            return company

        return None

    def create_company(self, company: CompanyCreate) -> Company:
        company = Company(
                    name = company.name,
                    address = company.address,
                    phone = company.phone,
                    email = company.email
                    )

        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def update_company(self, id: int, company: CompanyCreate) -> Company:
        c = self.db.query(Company).filter(Company.id == id).one()

        if c:
            c.name = company.name,
            c.address = company.address,
            c.phone = company.phone,
            c.email = company.email
            self.db.commit()
            return c

        return None

    def delete_company(self, id: int) -> int:
        result = self.db.query(Company).filter(Company.id == id).delete()
        self.db.commit()
        return result