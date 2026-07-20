from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.department import DepartmentCreate
from app.schemas.department import DepartmentUpdate
from app.schemas.department import DepartmentResponse

from app.services.department_service import DepartmentService


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def get_departments(
    db: Session = Depends(get_db)
):
    return DepartmentService.get_all(db)


@router.post(
    "",
    response_model=DepartmentResponse
)
def create_department(
    request: DepartmentCreate,
    db: Session = Depends(get_db)
):

    try:

        return DepartmentService.create(
            db,
            request
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: str,
    request: DepartmentUpdate,
    db: Session = Depends(get_db)
):

    try:

        return DepartmentService.update(
            db,
            department_id,
            request
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete(
    "/{department_id}"
)
def delete_department(
    department_id: str,
    db: Session = Depends(get_db)
):

    try:

        return DepartmentService.delete(
            db,
            department_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )