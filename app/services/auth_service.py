from sqlalchemy.orm import Session

from app.core.security import (hash_password,verify_password,create_access_token)
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

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):
        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        if not verify_password(
            password,
            user.hashed_password
        ):
            raise ValueError(
                "Invalid email or password"
            )

        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }