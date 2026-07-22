from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.user import UserResponse

from app.services.user_service import UserService

from app.schemas.user import UserUpdate

from app.database.dependencies import get_current_user
from app.models.user import User

from app.schemas.user import ChangePasswordRequest
from sqlalchemy.orm import relationship

from app.models.company import Company
from app.models.department import Department
from sqlalchemy import text

from app.database.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return UserService.get_all_users(db)

@router.get(
    "/me",
    response_model=UserResponse
)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return UserService.build_user_response(
        db,
        current_user
    )


@router.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:

        UserService.change_password(
            db,
            current_user,
            request.current_password,
            request.new_password
        )

        return {
            "message": "Password changed successfully."
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    user = UserService.get_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: str,
    request: UserUpdate,
    db: Session = Depends(get_db)
):

    try:

        return UserService.update_user(
            db,
            user_id,
            request
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.role not in ["ADMIN", "MANAGER"]:
        raise HTTPException(
            status_code=403,
            detail="Only Admin and Manager can delete employees."
        )

    try:
        return UserService.delete_user(
            db,
            user_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )