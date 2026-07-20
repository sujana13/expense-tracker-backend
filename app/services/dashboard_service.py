from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense

from app.models.category import Category

from app.models.enums import ExpenseStatus

import calendar

from app.models.user import User

class DashboardService:

    @staticmethod
    def apply_date_filter(query, from_date=None, to_date=None):
        if from_date:
            query = query.filter(
                Expense.expense_date >= from_date
            )

        if to_date:
            query = query.filter(
                Expense.expense_date <= to_date
            )

        return query

    @staticmethod
    def get_summary(
        db: Session,
        from_date: date | None = None,
        to_date: date | None = None,
       ):

        # Total Expenses
        total_query = db.query(
            func.coalesce(
                func.sum(Expense.amount),
                0
            )
        )

        total_query = DashboardService.apply_date_filter(
            total_query,
            from_date,
            to_date,
        )

        total_expenses = total_query.scalar()

        # Total Expense Count
        expense_query = db.query(Expense)

        expense_query = DashboardService.apply_date_filter(
            expense_query,
            from_date,
            to_date,
        )

        expense_count = expense_query.count()

        # Submitted
        submitted_query = db.query(Expense).filter(
            Expense.status == ExpenseStatus.SUBMITTED
        )

        submitted_query = DashboardService.apply_date_filter(
            submitted_query,
            from_date,
            to_date,
        )

        submitted_count = submitted_query.count()

        # Approved
        approved_query = db.query(Expense).filter(
            Expense.status == ExpenseStatus.APPROVED
        )

        approved_query = DashboardService.apply_date_filter(
            approved_query,
            from_date,
            to_date,
        )

        approved_count = approved_query.count()

        # Rejected
        rejected_query = db.query(Expense).filter(
            Expense.status == ExpenseStatus.REJECTED
        )

        rejected_query = DashboardService.apply_date_filter(
            rejected_query,
            from_date,
            to_date,
        )

        rejected_count = rejected_query.count()

        # Pending
        pending_query = db.query(Expense).filter(
            Expense.status == ExpenseStatus.SUBMITTED
        )

        pending_query = DashboardService.apply_date_filter(
            pending_query,
            from_date,
            to_date,
        )

        pending_count = pending_query.count()

        return {
            "total_expenses": total_expenses,
            "expense_count": expense_count,
            "this_month_total": total_expenses,
            "submitted_count": submitted_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "pending_approvals": pending_count,
        }

    @staticmethod
    def get_category_summary(
        db: Session,
        from_date: date | None = None,
        to_date: date | None = None,
    ):

        query = (
            db.query(
                 Category.name,
                 func.coalesce(
                    func.sum(Expense.amount),
                    0
                ).label("total_amount"),
            )
            .join(
               Expense,
               Expense.category_id == Category.id
            )
        )

        query = DashboardService.apply_date_filter(
            query,
            from_date,
            to_date,
        )

        results = (
             query
             .group_by(Category.name)
             .all()
        )

        return [
            {
               "category": row.name,
               "total_amount": row.total_amount,
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
        db: Session,
        from_date: date | None = None,
        to_date: date | None = None,
    ):

        query = db.query(

            func.extract(
                "month",
                Expense.expense_date,
            ).label("month"),

            func.coalesce(
                func.sum(Expense.amount),
                0,
            ).label("total_amount"),

        )

        query = DashboardService.apply_date_filter(
            query,
            from_date,
            to_date,
        )

        results = (
            query
            .group_by("month")
            .order_by("month")
            .all()
        )

        return [
            {
                "month": calendar.month_abbr[int(row.month)],
                "total_amount": row.total_amount,
            }
             for row in results
        ]

        
    @staticmethod
    def get_pending_count(db: Session):
        return (
            db.query(Expense)
            .filter(
            Expense.status == "SUBMITTED"
            )
           .count()
    )

    @staticmethod
    def get_employee_summary(
        db: Session,
        user_id: str
    ):

        total_expenses = (
            db.query(
                func.coalesce(
                   func.sum(Expense.amount),
                   0
                )
            )
            .filter(
                Expense.user_id == user_id
            )
            .scalar()
        )

        expense_count = (
            db.query(Expense)
               .filter(
               Expense.user_id == user_id
            )
            .count()
        )

        submitted_count = (
            db.query(Expense)
              .filter(
                 Expense.user_id == user_id,
            Expense.status == ExpenseStatus.SUBMITTED
            )
            .count()
        )

        approved_count = (
            db.query(Expense)
             .filter(
               Expense.user_id == user_id,
               Expense.status == ExpenseStatus.APPROVED
            )
             .count()
        )

        rejected_count = (
            db.query(Expense)
            .filter(
                Expense.user_id == user_id,
                Expense.status == ExpenseStatus.REJECTED
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
                Expense.user_id == user_id
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
            "rejected_count": rejected_count,
        }

    @staticmethod
    def get_employee_recent_expenses(
        db: Session,
        user_id: str,
        limit: int = 5
    ):

        return (
            db.query(Expense)
            .filter(
                Expense.user_id == user_id
            )
            .order_by(
                Expense.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_manager_summary(
        db: Session,
    ):

        team_expenses = (
            db.query(
                func.coalesce(
                   func.sum(Expense.amount),
                   0
                )
            )
            .scalar()
        )

        pending = (
            db.query(Expense)
            .filter(
                Expense.status == ExpenseStatus.SUBMITTED
            )
            .count()
            )

        approved = (
            db.query(Expense)
            .filter(
                Expense.status == ExpenseStatus.APPROVED
            )
            .count()
        )

        rejected = (
            db.query(Expense)
            .filter(
                 Expense.status == ExpenseStatus.REJECTED
            )
            .count()
        )

        return {
            "team_expenses": team_expenses,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        }


    @staticmethod
    def get_pending_approvals(
        db: Session,
        limit: int = 10,
    ):

        results = (
            db.query(
               Expense,
               User.username,
               Category.name
            )
            .join(
                User,
                User.id == Expense.user_id
            )
            .outerjoin(
                Category,
                Category.id == Expense.category_id
            )
            .filter(
                Expense.status == ExpenseStatus.SUBMITTED
             )
            .order_by(
                Expense.created_at.desc()
            )
            .limit(limit)
            .all()
        )

        response = []

        for expense, username, category in results:

            response.append(
               {
                    "id": expense.id,
                    "employee_name": username,
                    "title": expense.title,
                    "amount": expense.amount,
                    "expense_date": expense.expense_date,
                    "status": expense.status.value if hasattr(expense.status, "value") else expense.status,
                    "category_name": category,
                }
            )

        return response   

    @staticmethod
    def get_finance_summary(db: Session):

        total_expenses = (
            db.query(
                func.coalesce(
                   func.sum(Expense.amount),
                   0
                )
            )
            .scalar()
        )

        pending_payments = (
            db.query(Expense)
               .filter(
                   Expense.status == ExpenseStatus.APPROVED
                )
            .count()
            )

        completed_payments = (
            db.query(Expense)
               .filter(
                    Expense.status == ExpenseStatus.PAID
                )
             .count()
            )

        current_month = date.today().month
        current_year = date.today().year

        paid_this_month = (
            db.query(
                func.coalesce(
                     func.sum(Expense.amount),
                     0
                    )
                 )
                .filter(
                  Expense.status == ExpenseStatus.PAID
                 )
               .filter(
                   func.extract(
                   "month",
                    Expense.paid_at
                    ) == current_month
                )
                .filter(
                     func.extract(
                     "year",
                     Expense.paid_at
                    ) == current_year
                 )
                .scalar()
                )

        return {
            "total_expenses": total_expenses,
            "pending_payments": pending_payments,
            "paid_this_month": paid_this_month,
            "completed_payments": completed_payments,
        }     


    @staticmethod
    def get_approved_expenses(
        db: Session,
        limit: int = 5,
    ):
        expenses = (
            db.query(Expense)
            .filter(
               Expense.status == ExpenseStatus.APPROVED
            )
            .order_by(
               Expense.approved_at.desc()
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "id": expense.id,
                "title": expense.title,
                "employee_name": expense.submitted_by_name,
                "category_name": expense.category.name if expense.category else "-",
                "amount": expense.amount,
                "expense_date": expense.expense_date,
                "status": expense.status.value,
            }
            for expense in expenses
        ]

    @staticmethod
    def get_admin_summary(
        db: Session,
    ):
        total_employees = (
            db.query(User)
            .count()
        )

        total_expenses = (
            db.query(
                func.coalesce(
                    func.sum(Expense.amount),
                    0
                )
            )
            .scalar()
        )

        pending_approvals = (
            db.query(Expense)
            .filter(
                 Expense.status == ExpenseStatus.SUBMITTED
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
            "total_employees": total_employees,
            "total_expenses": total_expenses,
            "pending_approvals": pending_approvals,
            "this_month_total": this_month_total,
        }