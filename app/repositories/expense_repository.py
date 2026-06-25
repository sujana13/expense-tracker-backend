from sqlalchemy.orm import Session

from app.models.expense import Expense
from datetime import date

from sqlalchemy import or_

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
        end_date: date | None = None,
        search: str | None = None
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

        if search:
            query = query.filter(
               or_(
            Expense.title.ilike(
                f"%{search}%"
            ),
            Expense.description.ilike(
                f"%{search}%"
            ),
            Expense.payment_method.ilike(
                f"%{search}%"
            )
        )
    )

        return query.all()

    @staticmethod
    def get_all_for_export(
        db: Session
    ):
        return (
            db.query(Expense)
            .order_by(
            Expense.expense_date.desc()
        )
        .all()
    )

    @staticmethod
    def get_by_user_id(
    db: Session,
    user_id: str
    ):
        return (
            db.query(Expense)
            .filter(
            Expense.user_id == user_id
            )
            .all()
        )