from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme
from app.core.security import decode_access_token

from app.database.dependencies import get_db

from app.repositories.user_repository import UserRepository

from app.core.permissions import is_admin


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = UserRepository.get_by_email(
        db,
        email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user 

def require_admin(
    current_user = Depends(get_current_user)
):
    if not is_admin(current_user):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user