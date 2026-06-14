from pydantic import BaseModel

from datetime import date

class DashboardSummary(BaseModel):
    total_expenses: float
    expense_count: int
    this_month_total: float

class CategorySummary(BaseModel):
    category: str
    total_amount: float

class RecentExpense(BaseModel):
    id: str
    title: str
    amount: float
    expense_date: date