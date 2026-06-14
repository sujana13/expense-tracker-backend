from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_expenses: float
    expense_count: int
    this_month_total: float

class CategorySummary(BaseModel):
    category: str
    total_amount: float