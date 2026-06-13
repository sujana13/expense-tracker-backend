from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.user import User

from app.repositories.expense_repository import ExpenseRepository
from app.repositories.category_repository import CategoryRepository

from app.schemas.expense import ExpenseCreate
from app.schemas.expense import ExpenseUpdate


class ExpenseService:

    @staticmethod
    def create(
        db: Session,
        request: ExpenseCreate,
        current_user: User
    ):
        category = CategoryRepository.get_by_id(
            db,
            request.category_id
        )

        if not category:
            raise ValueError(
                "Category not found"
            )

        expense = Expense(
            title=request.title,
            description=request.description,
            amount=request.amount,
            expense_date=request.expense_date,
            payment_method=request.payment_method,
            category_id=request.category_id,
            user_id=current_user.id
        )

        return ExpenseRepository.create(
            db,
            expense
        )

    @staticmethod
    def get_all(
        db: Session
    ):
        return ExpenseRepository.get_all(db)

    @staticmethod
    def get_by_id(
        db: Session,
        expense_id: str
    ):
        expense = ExpenseRepository.get_by_id(
            db,
            expense_id
        )

        if not expense:
            raise ValueError(
                "Expense not found"
            )

        return expense

    @staticmethod
    def delete(
        db: Session,
        expense_id: str
    ):
        expense = ExpenseRepository.get_by_id(
            db,
            expense_id
        )

        if not expense:
            raise ValueError(
                "Expense not found"
            )

        ExpenseRepository.delete(
            db,
            expense
        )