from sqlalchemy.orm import Session

from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate
from app.schemas.company import CompanyUpdate


class CompanyService:

    @staticmethod
    def get_all(db: Session):
        return CompanyRepository.get_all(db)

    @staticmethod
    def create(
        db: Session,
        request: CompanyCreate
    ):

        existing = CompanyRepository.get_by_name(
            db,
            request.name
        )

        if existing:
            raise ValueError(
                "Company already exists."
            )

        company = Company(
            name=request.name
        )

        return CompanyRepository.create(
            db,
            company
        )

    @staticmethod
    def update(
        db: Session,
        company_id: str,
        request: CompanyUpdate
    ):

        company = CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise ValueError(
                "Company not found."
            )

        company.name = request.name
        company.is_active = request.is_active

        return CompanyRepository.update(
            db,
            company
        )

    @staticmethod
    def delete(
        db: Session,
        company_id: str
    ):

        company = CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise ValueError(
                "Company not found."
            )

        CompanyRepository.delete(
            db,
            company
        )

        return {
            "message": "Company deleted successfully."
        }