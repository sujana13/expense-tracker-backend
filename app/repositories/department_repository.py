from sqlalchemy.orm import Session

from app.models.department import Department


class DepartmentRepository:

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Department)
            .order_by(Department.name)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        department_id: str
    ):
        return (
            db.query(Department)
            .filter(Department.id == department_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str
    ):
        return (
            db.query(Department)
            .filter(Department.name == name)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        department: Department
    ):
        db.add(department)
        db.commit()
        db.refresh(department)
        return department

    @staticmethod
    def update(
        db: Session,
        department: Department
    ):
        db.commit()
        db.refresh(department)
        return department

    @staticmethod
    def delete(
        db: Session,
        department: Department
    ):
        db.delete(department)
        db.commit()