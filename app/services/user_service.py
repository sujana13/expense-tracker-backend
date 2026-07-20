from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository 

from app.schemas.user import UserUpdate

from app.models.user import User

from app.core.security import (
    verify_password,
    hash_password
)
from app.schemas.user import UserResponse
from app.models.company import Company
from app.models.department import Department

class UserService:



    @staticmethod
    def get_all_users(
        db: Session
    ):

        users = UserRepository.get_all(db)

        return [
            UserService.build_user_response(
            db,
            user
            )
            for user in users
        ]


    @staticmethod
    def get_user(
       db: Session,
       user_id: str
    ):

        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            return None

        return UserService.build_user_response(
           db,
           user
        )


    @staticmethod
    def delete_user(
        db: Session,
        user_id: str
    ):

        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise ValueError(
                "User not found"
            )

        UserRepository.delete(
            db,
            user
        )

        return {
            "message": "User deleted successfully"
        }

    @staticmethod
    def update_user(
        db: Session,
        user_id: str,
        request: UserUpdate
    ):

        user = UserRepository.get_by_id(
        db,
        user_id
    )

        if not user:
            raise ValueError(
            "User not found"
        )

        user.username = request.username
        user.role = request.role.value

        user.employee_id = request.employee_id
        user.position = request.position
        user.phone = request.phone
        user.gender = request.gender
        user.location = request.location
        user.birth_date = request.birth_date
        user.date_of_joining = request.date_of_joining

        user.is_active = request.is_active
        user.company_id = request.company_id
        user.department_id = request.department_id

        return UserRepository.update(
           db,
           user
    )

    @staticmethod
    def change_password(
        db: Session,
        current_user: User,
        current_password: str,
        new_password: str
    ):

        if not verify_password(
            current_password,
            current_user.hashed_password
        ):
            raise ValueError(
            "Current password is incorrect."
            )

        current_user.hashed_password = hash_password(
            new_password
        )

        return UserRepository.update_password(
            db,
            current_user
        )

    @staticmethod
    def build_user_response(
        db: Session,
        user: User
):

        company = (
            db.query(Company)
            .filter(Company.id == user.company_id)
            .first()
    )

        department = (
            db.query(Department)
            .filter(Department.id == user.department_id)
            .first()
        )

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,

            company_id=user.company_id,
            department_id=user.department_id,

            company_name=company.name if company else None,
            department_name=department.name if department else None,

            employee_id=user.employee_id,
            position=user.position,
            phone=user.phone,
            gender=user.gender,
            location=user.location,
            birth_date=user.birth_date,
            date_of_joining=user.date_of_joining,
        )