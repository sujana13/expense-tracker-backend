from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.company import CompanyCreate
from app.schemas.company import CompanyUpdate
from app.schemas.company import CompanyResponse

from app.services.company_service import CompanyService


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.get(
    "",
    response_model=list[CompanyResponse]
)
def get_companies(
    db: Session = Depends(get_db)
):

    return CompanyService.get_all(db)


@router.post(
    "",
    response_model=CompanyResponse
)
def create_company(
    request: CompanyCreate,
    db: Session = Depends(get_db)
):

    try:

        return CompanyService.create(
            db,
            request
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put(
    "/{company_id}",
    response_model=CompanyResponse
)
def update_company(
    company_id: str,
    request: CompanyUpdate,
    db: Session = Depends(get_db)
):

    try:

        return CompanyService.update(
            db,
            company_id,
            request
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete(
    "/{company_id}"
)
def delete_company(
    company_id: str,
    db: Session = Depends(get_db)
):

    try:

        return CompanyService.delete(
            db,
            company_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )