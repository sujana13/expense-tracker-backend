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

from app.database.dependencies import get_current_user
from app.models.user import User

from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import ForgotPasswordRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
async def register(
    request: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    allowed_domain = "@higheredbpo.co.in"

    if not request.email.lower().endswith(allowed_domain):
        raise HTTPException(
           status_code=400,
           detail=f"Only {allowed_domain} email addresses are allowed."
       )

    if current_user.role not in ["ADMIN", "MANAGER"]:
        raise HTTPException(
            status_code=403,
            detail="Only Admin and Manager can add employees."
        )

    try:
        return await AuthService.register(
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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        return AuthService.login(
            db,
            form_data.username,
            form_data.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    return AuthService.forgot_password(
        db,
        request.email
    )