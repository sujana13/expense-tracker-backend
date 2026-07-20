from sqlalchemy.orm import Session

from app.models.department import Department
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department import DepartmentCreate
from app.schemas.department import DepartmentUpdate


class DepartmentService:

    @staticmethod
    def get_all(db: Session):
        return DepartmentRepository.get_all(db)

    @staticmethod
    def create(
        db: Session,
        request: DepartmentCreate
    ):

        existing = DepartmentRepository.get_by_name(
            db,
            request.name
        )

        if existing:
            raise ValueError(
                "Department already exists."
            )

        department = Department(
            name=request.name
        )

        return DepartmentRepository.create(
            db,
            department
        )

    @staticmethod
    def update(
        db: Session,
        department_id: str,
        request: DepartmentUpdate
    ):

        department = DepartmentRepository.get_by_id(
            db,
            department_id
        )

        if not department:
            raise ValueError(
                "Department not found."
            )

        department.name = request.name
        department.is_active = request.is_active

        return DepartmentRepository.update(
            db,
            department
        )

    @staticmethod
    def delete(
        db: Session,
        department_id: str
    ):

        department = DepartmentRepository.get_by_id(
            db,
            department_id
        )

        if not department:
            raise ValueError(
                "Department not found."
            )

        DepartmentRepository.delete(
            db,
            department
        )

        return {
            "message": "Department deleted successfully."
        }