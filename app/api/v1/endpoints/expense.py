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
    db: Session = Depends(get_db)
):
    return ExpenseService.get_all(db)

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(
    expense_id: str,
    db: Session = Depends(get_db)
):
    try:
        return ExpenseService.get_by_id(
            db,
            expense_id
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
    db: Session = Depends(get_db)
):
    try:
        ExpenseService.delete(
            db,
            expense_id
        )

        return {
            "message": "Expense deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )