from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.dependencies import get_current_user

from app.models.user import User

from app.schemas.expense import ExpenseCreate
from app.schemas.expense import ExpenseResponse

from app.services.expense_service import ExpenseService

from app.schemas.expense import ExpenseUpdate 

from datetime import date
from fastapi import Query

from fastapi.responses import Response

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post(
    "",
    response_model=ExpenseResponse
)
def create_expense(
    request: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ExpenseService.create(
            db,
            request,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "",
    response_model=list[ExpenseResponse]
)
def get_expenses(
    category_id: str | None = Query(None),
    payment_method: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if (
    category_id
    or payment_method
    or start_date
    or end_date
    or search
):
        return ExpenseService.filter_expenses(
            db,
            category_id,
            payment_method,
            start_date,
            end_date,
            search
        )

    return ExpenseService.get_all(
    db,
    current_user
)

@router.get(
    "/export"
)
def export_expenses(
    db: Session = Depends(get_db)
):
    csv_data = (
        ExpenseService.export_csv(
            db
        )
    )

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=expenses.csv"
        }
    )

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(
    expense_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

    ):
    try:
        return ExpenseService.get_by_id(
            db,
            expense_id,
                current_user

        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.delete(
    "/{expense_id}"
)
def delete_expense(
    expense_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        ExpenseService.delete(
            db,
            expense_id,
            current_user
        )

        return {
            "message": "Expense deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense(
    expense_id: str,
    request: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ExpenseService.update(
            db,
            expense_id,
            request,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.post(
    "/{expense_id}/approve",
    response_model=ExpenseResponse
)
def approve_expense(
    expense_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ExpenseService.approve_expense(
            db,
            expense_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post(
    "/{expense_id}/reject",
    response_model=ExpenseResponse
)
def reject_expense(
    expense_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ExpenseService.reject_expense(
            db,
            expense_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )