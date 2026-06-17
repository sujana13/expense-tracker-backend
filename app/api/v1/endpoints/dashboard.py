from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.dashboard import DashboardSummary

from app.services.dashboard_service import DashboardService

from app.schemas.dashboard import CategorySummary

from app.schemas.dashboard import RecentExpense

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

@router.get(
    "/recent-expenses",
    response_model=list[RecentExpense]
)
def get_recent_expenses(
    db: Session = Depends(get_db)
):
    return DashboardService.get_recent_expenses(
        db
    )

@router.get(
    "/monthly-trend"
)
def get_monthly_trend(
    db: Session = Depends(get_db)
):
    return DashboardService.get_monthly_trend(
        db
    )