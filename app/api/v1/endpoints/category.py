from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryUpdate
from app.schemas.category import CategoryResponse
from app.services.category_service import CategoryService

from app.core.auth import require_admin


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post(
    "",
    response_model=CategoryResponse
)
def create_category(
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    try:
        return CategoryService.create(
            db,
            request
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "",
    response_model=list[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    return CategoryService.get_all(db)

@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    try:
        return CategoryService.get_by_id(
            db,
            category_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: str,
    request: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    try:
        return CategoryService.update(
            db,
            category_id,
            request
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.delete(
    "/{category_id}"
)
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    try:
        CategoryService.delete(
            db,
            category_id
        )

        return {
            "message": "Category deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
                