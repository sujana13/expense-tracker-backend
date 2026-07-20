from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.dashboard import DashboardSummary

from app.services.dashboard_service import DashboardService

from app.schemas.dashboard import CategorySummary

from app.schemas.dashboard import RecentExpense

from app.database.dependencies import get_current_user

from app.schemas.dashboard import EmployeeDashboardSummary

from app.models.user import User

from app.schemas.dashboard import ManagerDashboardSummary 

from app.schemas.dashboard import PendingApprovalResponse

from app.schemas.dashboard import FinanceDashboardSummary

from app.schemas.dashboard import AdminDashboardSummary
from datetime import date


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)



@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService.get_summary(
        db=db,
        from_date=from_date,
        to_date=to_date,
    )

@router.get(
    "/category-summary",
    response_model=list[CategorySummary]
)
def get_category_summary(
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService.get_category_summary(
        db=db,
        from_date=from_date,
        to_date=to_date,
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

@router.get("/monthly-trend")
def get_monthly_trend(
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService.get_monthly_trend(
        db=db,
        from_date=from_date,
        to_date=to_date,
    )

@router.get(
    "/employee-summary",
    response_model=EmployeeDashboardSummary
)
def get_employee_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return DashboardService.get_employee_summary(
        db,
        current_user.id
    )

@router.get(
    "/employee-recent-expenses",
    response_model=list[RecentExpense]
)
def get_employee_recent_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return DashboardService.get_employee_recent_expenses(
        db,
        current_user.id
    )

@router.get(
    "/manager-summary",
    response_model=ManagerDashboardSummary,
)
def get_manager_summary(
    db: Session = Depends(get_db),
):

    return DashboardService.get_manager_summary(db)

@router.get(
    "/pending-approvals",
    response_model=list[PendingApprovalResponse],
)
def get_pending_approvals(
    db: Session = Depends(get_db),
):

    return DashboardService.get_pending_approvals(db)

@router.get(
    "/finance-summary",
    response_model=FinanceDashboardSummary
)
def get_finance_summary(
    db: Session = Depends(get_db)
):
    return DashboardService.get_finance_summary(db)

@router.get("/approved-expenses")
def get_approved_expenses(
    db: Session = Depends(get_db),
):
    return DashboardService.get_approved_expenses(db)

@router.get(
    "/admin-summary",
    response_model=AdminDashboardSummary,
)
def get_admin_summary(
    db: Session = Depends(get_db),
):
    return DashboardService.get_admin_summary(db)