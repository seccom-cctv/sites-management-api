from schemas.company import Company, CompanyCreate

from services.main import AppService, AppCRUD

class CompanyService(AppService):
    def create(self, company: CompanyCreate):
        company = CompanyCRUD(self.db).create(company)
        if not company:
            return "TODOexception"
        return company

    def get(self, id: int):
        company = CompanyCRUD(self.db).get(id)
        if not company:
            return "TODOexception"
        return company


class CompanyCRUD(AppCRUD):
    def create(self, company: CompanyCreate) -> Company:
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get(self, id: int) -> Company:
        company = self.db.query(Company).filter(Company.id == id).first()
        if company:
            return company
        return None