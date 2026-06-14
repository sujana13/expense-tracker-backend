from sqlalchemy.orm import Session

from app.models.expense import Expense
from datetime import date

class ExpenseRepository:

    @staticmethod
    def create(
        db: Session,
        expense: Expense
    ):
        db.add(expense)
        db.commit()
        db.refresh(expense)

        return expense

    @staticmethod
    def get_all(
        db: Session
    ):
        return db.query(Expense).all()

    @staticmethod
    def get_by_id(
        db: Session,
        expense_id: str
    ):
        return (
            db.query(Expense)
            .filter(Expense.id == expense_id)
            .first()
        )

    @staticmethod
    def delete(
        db: Session,
        expense: Expense
    ):
        db.delete(expense)
        db.commit()

    @staticmethod
    def update(
        db: Session,
        expense: Expense
    ):
        db.commit()
        db.refresh(expense)

        return expense 

    @staticmethod
    def filter_expenses(
        db: Session,
        category_id: str | None = None,
        payment_method: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None
    ):
        query = db.query(Expense)

        if category_id:
            query = query.filter(
                Expense.category_id == category_id
            )

        if payment_method:
            query = query.filter(
                Expense.payment_method == payment_method
            )

        if start_date:
            query = query.filter(
                Expense.expense_date >= start_date
            )

        if end_date:
            query = query.filter(
                Expense.expense_date <= end_date
            )

        return query.all()