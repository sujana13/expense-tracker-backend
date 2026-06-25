from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense

from app.models.category import Category

from app.models.enums import ExpenseStatus

import calendar

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

        submitted_count = (
            db.query(Expense)
            .filter(
                Expense.status ==
                   ExpenseStatus.SUBMITTED
                )
            .count()
            )

        approved_count = (
            db.query(Expense)
            .filter(
                Expense.status ==
                  ExpenseStatus.APPROVED
                )
            .count()
        )

        rejected_count = (
            db.query(Expense)
            .filter(
               Expense.status ==
                 ExpenseStatus.REJECTED
            )
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
            "this_month_total": this_month_total,

            "submitted_count": submitted_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count
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

    @staticmethod
    def get_recent_expenses(
        db: Session,
        limit: int = 5
    ):
        expenses = (
            db.query(Expense)
            .order_by(
            Expense.created_at.desc()
        )
        .limit(limit)
        .all()
    )

        return expenses

    @staticmethod
    def get_monthly_trend(
        db: Session
):
        results = (
            db.query(
               func.extract(
                "month",
                Expense.expense_date
            ).label("month"),

            func.coalesce(
                func.sum(
                    Expense.amount
                ),
                0
            ).label(
                "total_amount"
            )
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

        return [
            {
               "month": calendar.month_abbr[int(row.month)],
               "total_amount": row.total_amount
            }
        for row in results
    ]