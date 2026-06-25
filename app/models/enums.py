from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class ExpenseStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"