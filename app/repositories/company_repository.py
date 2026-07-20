from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Company)
            .order_by(Company.name)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        company_id: str
    ):
        return (
            db.query(Company)
            .filter(Company.id == company_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str
    ):
        return (
            db.query(Company)
            .filter(Company.name == name)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        company: Company
    ):
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    @staticmethod
    def update(
        db: Session,
        company: Company
    ):
        db.commit()
        db.refresh(company)
        return company

    @staticmethod
    def delete(
        db: Session,
        company: Company
    ):
        db.delete(company)
        db.commit()