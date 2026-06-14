from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense

from app.models.category import Category

class DashboardService:

    @staticmethod
    def get_summary(
        db: Session
    ):
        total_expenses = (
            db.query(
                func.coalesce(
                    func.sum(Expense.amount),
                    0
                )
            )
            .scalar()
        )

        expense_count = (
            db.query(Expense)
            .count()
        )

        current_month = date.today().month
        current_year = date.today().year

        this_month_total = (
            db.query(
                func.coalesce(
                    func.sum(Expense.amount),
                    0
                )
            )
            .filter(
                func.extract(
                    "month",
                    Expense.expense_date
                ) == current_month
            )
            .filter(
                func.extract(
                    "year",
                    Expense.expense_date
                ) == current_year
            )
            .scalar()
        )

        return {
            "total_expenses": total_expenses,
            "expense_count": expense_count,
            "this_month_total": this_month_total
        }

    @staticmethod
    def get_category_summary(
        db: Session
         ):
        results = (
                db.query(
                Category.name,
                func.coalesce(
                func.sum(Expense.amount),
                0
                )
             )
        .join(
                Expense,
                Expense.category_id == Category.id
            )
        .group_by(
                Category.name
            )
        .all()
            )

        return [
            {
                "category": row[0],
                "total_amount": row[1]
            }
        for row in results
    ]