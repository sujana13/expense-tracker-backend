from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:

    @staticmethod
    def register(
        db: Session,
        request: UserCreate
    ):
        existing_user = (
            UserRepository.get_by_email(
                db,
                request.email
            )
        )

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        user = User(
            username=request.username,
            email=request.email,
            hashed_password=hash_password(
                request.password
            ),
            role=request.role.value
        )

        return UserRepository.create(
            db,
            user
        )