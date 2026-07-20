from datetime import date
from pydantic import BaseModel, ConfigDict


class DashboardSummary(BaseModel):
    total_expenses: float
    expense_count: int
    this_month_total: float

    submitted_count: int
    approved_count: int
    rejected_count: int

    pending_approvals: int

class EmployeeDashboardSummary(BaseModel):
    total_expenses: float
    expense_count: int
    this_month_total: float

    submitted_count: int
    approved_count: int
    rejected_count: int

class CategorySummary(BaseModel):
    category: str
    total_amount: float

class RecentExpense(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    amount: float
    expense_date: date
    status: str

class ManagerDashboardSummary(BaseModel):
    team_expenses: float

    pending: int
    approved: int
    rejected: int

class PendingApprovalResponse(BaseModel):
    id: str
    employee_name: str
    title: str
    amount: float
    expense_date: date
    status: str
    category_name: str | None = None

class FinanceDashboardSummary(BaseModel):
    total_expenses: float
    pending_payments: int
    paid_this_month: float
    completed_payments: int

class AdminDashboardSummary(BaseModel):
    total_employees: int
    total_expenses: float
    pending_approvals: int
    this_month_total: float