from sqlalchemy.exc import SQLAlchemyError
from app.schemas.company import CompanyCreate
from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.models.company import Company
from app.utils.service_result import ServiceResult
from typing import List


class CompanyService(AppService):
    def get_company(self, id: int) -> ServiceResult:
        result = CompanyCRUD(self.db).get_company(id)
        if not isinstance(result, list):
            return ServiceResult(AppException.Get({"id_not_found": id}))
        #if not company.public:
            # return ServiceResult(AppException.RequiresAuth())
        return ServiceResult(result)

    def create_company(self, company: CompanyCreate) -> ServiceResult:
        result = CompanyCRUD(self.db).create_company(company)
        if not isinstance(result, Company):
            return ServiceResult(AppException.Create(result))
        return ServiceResult(result)

    def update_company(self, id: int, company: CompanyCreate) -> ServiceResult:
        result = CompanyCRUD(self.db).update_company(id, company)
        if not isinstance(result, Company):
            return ServiceResult(AppException.Update(result))
        return ServiceResult(result)

    def delete_company(self, id: int) -> ServiceResult:
        result = CompanyCRUD(self.db).delete_company(id)
        if result == 0:
            return ServiceResult(AppException.Delete({"deleted_rows": result}))
        return ServiceResult({"deleted_rows": result})


class CompanyCRUD(AppCRUD):
    def get_company(self, id: int) -> List[Company]:
        if id:
            companies = self.db.query(Company).filter(Company.id == id).first()
            companies = [companies] # returns list
        else:
            companies = self.db.query(Company).all()

        return companies

    def create_company(self, company: CompanyCreate) -> Company:
        company = Company(
                    name = company.name,
                    address = company.address,
                    phone = company.phone,
                    email = company.email
                    )
        try:
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)
        except SQLAlchemyError as e:
            return str(e)

        return company

    def update_company(self, id: int, company: CompanyCreate) -> Company:
        try:
            c = self.db.query(Company).filter(Company.id == id).one()
            c.name = company.name,
            c.address = company.address,
            c.phone = company.phone,
            c.email = company.email
            self.db.commit()
        except SQLAlchemyError as e:
            return str(e)

        return c

    def delete_company(self, id: int) -> int:
        result = self.db.query(Company).filter(Company.id == id).delete()
        self.db.commit()
        return result