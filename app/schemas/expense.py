from datetime import date

from pydantic import BaseModel

from app.models.enums import ExpenseStatus

from datetime import datetime



class ExpenseCreate(BaseModel):
    title: str
    description: str | None = None
    amount: float
    expense_date: date
    payment_method: str
    category_id: str


class ExpenseUpdate(BaseModel):
    title: str
    description: str | None = None
    amount: float
    expense_date: date
    payment_method: str
    category_id: str


class ExpenseResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    amount: float
    expense_date: date
    payment_method: str
    category_name: str | None = None
    category_id: str
    user_id: str
    receipt_path: str | None = None
    status: ExpenseStatus

    approved_by: str | None = None
    approved_by_name: str | None = None
    approved_at: datetime | None = None

    rejected_by: str | None = None
    rejected_by_name: str | None = None
    rejected_at: datetime | None = None

    rejection_reason: str | None = None

    paid_by: str | None = None
    paid_by_name: str | None = None
    paid_at: datetime | None = None
    payment_reference: str | None = None
    payment_notes: str | None = None

    submitted_by_name: str | None = None

    

    model_config = {
        "from_attributes": True
    }

class ExpensePayment(BaseModel):
    payment_reference: str
    payment_notes: str | None = None

