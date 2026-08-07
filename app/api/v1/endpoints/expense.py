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

from fastapi import Form
from fastapi import File
from fastapi import UploadFile

from pathlib import Path
import shutil

import uuid
from fastapi.responses import StreamingResponse
from app.models.enums import UserRole
from app.schemas.expense import ExpensePayment
from app.utils.cloudinary_service import upload_receipt
from fastapi import BackgroundTasks
from app.repositories.category_repository import CategoryRepository
from app.services.email_service import EmailService

from app.schemas.expense import RejectExpenseRequest

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
}

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("", response_model=ExpenseResponse)
def create_expense(
    title: str = Form(...),
    description: str | None = Form(None),
    amount: float = Form(...),
    expense_date: date = Form(...),
    payment_method: str = Form(...),
    category_id: str = Form(...),
    receipt: UploadFile | None = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        receipt_path = None

        if receipt and receipt.filename:
            extension = Path(receipt.filename).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail="Only PDF, JPG, JPEG and PNG files are allowed.",
                )

            receipt_path = upload_receipt(receipt.file)

        created_expense = ExpenseService.create(
            db=db,
            title=title,
            description=description,
            amount=amount,
            expense_date=expense_date,
            payment_method=payment_method,
            category_id=category_id,
            receipt_path=receipt_path,
            current_user=current_user,
        )

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        background_tasks.add_task(
            EmailService.send_expense_created_email,
            email=current_user.email,
            username=current_user.username,
            title=created_expense.title,
            category=category.name if category else "N/A",
            amount=created_expense.amount,
            expense_date=str(created_expense.expense_date),
            payment_method=created_expense.payment_method,
            status=created_expense.status.value,
        )

        return created_expense

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
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
    current_user: User = Depends(get_current_user),
    status: str | None = Query(None),
):
   
    if (
    category_id
    or payment_method
    or start_date
    or end_date
    or search
    or status
):
        return ExpenseService.filter_expenses(
           db=db,
           category_id=category_id,
           payment_method=payment_method,
           start_date=start_date,
           end_date=end_date,
            search=search,
           status=status,
           current_user=current_user,
)
    return ExpenseService.get_all(
    db,
    current_user
)

@router.get("/export")
def export_csv(
    category: str | None = None,
    payment_method: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    search: str | None = None,

    db: Session = Depends(get_db),
):
    csv_data = ExpenseService.export_csv(
        db=db,
        category=category,
        payment_method=payment_method,
        from_date=from_date,
        to_date=to_date,
        search=search,
    )

    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=expenses.csv"
        },
    )


@router.get(
    "/payment-history",
    response_model=list[ExpenseResponse]
)
def payment_history(
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ExpenseService.get_paid_expenses(
        db,
        search=search,
    )

@router.get(
    "",
    response_model=list[ExpenseResponse]
)
def get_expenses(
    category_id: str | None = Query(None),
    payment_method: str | None = Query(None),

    from_date: date | None = Query(None),
    to_date: date | None = Query(None),

    search: str | None = Query(None),
    status: str | None = Query(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if (
        category_id
        or payment_method
        or from_date
        or to_date
        or search
        or status
    ):

        return ExpenseService.filter_expenses(
            db=db,
            category_id=category_id,
            payment_method=payment_method,
            start_date=from_date,
            end_date=to_date,
            search=search,
            status=status,
            current_user=current_user,
        )

    return ExpenseService.get_all(
        db,
        current_user,
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

    title: str = Form(...),
    description: str | None = Form(None),
    amount: float = Form(...),
    expense_date: date = Form(...),
    payment_method: str = Form(...),
    category_id: str = Form(...),
    receipt: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    receipt_path = None

    if receipt and receipt.filename:

        extension = Path(receipt.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, JPEG and PNG files are allowed."
        )

        receipt_path = upload_receipt(receipt.file)

    try:
        return ExpenseService.update(
            db=db,
            expense_id=expense_id,
            title=title,
            description=description,
            amount=amount,
            expense_date=expense_date,
            payment_method=payment_method,
            category_id=category_id,
            receipt_path=receipt_path,
            current_user=current_user,
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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ExpenseService.approve_expense(
            db,
            expense_id,
            current_user,
            background_tasks,
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
    background_tasks: BackgroundTasks,
    rejection_reason: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ExpenseService.reject_expense(
            db,
            expense_id,
            current_user,
            rejection_reason=rejection_reason,
            background_tasks=background_tasks,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post(
    "/{expense_id}/pay",
    response_model=ExpenseResponse
)
def mark_as_paid(
    expense_id: str,
    request: ExpensePayment,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return ExpenseService.mark_as_paid(
            db=db,
            expense_id=expense_id,
            payment_reference=request.payment_reference,
            payment_notes=request.payment_notes,
            current_user=current_user,
            background_tasks=background_tasks,

        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

