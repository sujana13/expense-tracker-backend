from datetime import date

from pydantic import BaseModel


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
    category_id: str
    user_id: str

    model_config = {
        "from_attributes": True
    }