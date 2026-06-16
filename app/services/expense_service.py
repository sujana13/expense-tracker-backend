from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.user import User

from app.repositories.expense_repository import ExpenseRepository
from app.repositories.category_repository import CategoryRepository

from app.schemas.expense import ExpenseCreate
from app.schemas.expense import ExpenseUpdate

from app.schemas.expense import ExpenseUpdate

from datetime import date

import csv
from io import StringIO


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

    @staticmethod
    def update(
        db: Session,
        expense_id: str,
        request: ExpenseUpdate
    ):
        expense = ExpenseRepository.get_by_id(
        db,
        expense_id
    )

        if not expense:
            raise ValueError(
            "Expense not found"
        )

        category = CategoryRepository.get_by_id(
                 db,
                 request.category_id
    )

        if not category:
             raise ValueError(
                 "Category not found"
        )

        expense.title = request.title
        expense.description = request.description
        expense.amount = request.amount
        expense.expense_date = request.expense_date
        expense.payment_method = request.payment_method
        expense.category_id = request.category_id

        return ExpenseRepository.update(
        db,
        expense
    )

    @staticmethod
    def filter_expenses(
        db: Session,
        category_id: str | None = None,
        payment_method: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        search: str | None = None
    ):
        return ExpenseRepository.filter_expenses(
            db,
            category_id,
            payment_method,
            start_date,
            end_date,
            search
        )

    @staticmethod
    def export_csv(
        db: Session
    ):
        expenses = (
            ExpenseRepository.get_all_for_export(
            db
        )
        )

        output = StringIO()

        writer = csv.writer(
        output
        )

        writer.writerow([
            "Title",
            "Description",
            "Amount",
            "Payment Method",
            "Expense Date"
        ])

        for expense in expenses:
            writer.writerow([
                expense.title,
                expense.description,
                expense.amount,
                expense.payment_method,
                expense.expense_date
            ])

        return output.getvalue()