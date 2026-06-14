from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.dashboard import DashboardSummary

from app.services.dashboard_service import DashboardService

from app.schemas.dashboard import CategorySummary

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummary
)
def get_summary(
    db: Session = Depends(get_db)
):
    return DashboardService.get_summary(
        db
    )

@router.get(
    "/category-summary",
    response_model=list[CategorySummary]
)
def get_category_summary(
    db: Session = Depends(get_db)
):
    return DashboardService.get_category_summary(
        db
    )