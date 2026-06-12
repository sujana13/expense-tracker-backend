from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

from app.schemas.user import UserLogin
from app.schemas.user import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    request: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return AuthService.register(
            db,
            request
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        return AuthService.login(
            db,
            request.email,
            request.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )