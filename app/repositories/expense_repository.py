from sqlalchemy.orm import Session

from app.models.expense import Expense
from datetime import date

from sqlalchemy import or_
from app.models.user import User

from app.models.enums import ExpenseStatus
from sqlalchemy.orm import joinedload

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
        return (
            db.query(Expense)
              .options(
            joinedload(Expense.submitted_by_user),   
            joinedload(Expense.category),            

            joinedload(Expense.approved_by_user),
            joinedload(Expense.rejected_by_user),
            joinedload(Expense.paid_by_user),
        )
        .all()
)

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
        search: str | None = None,
        status: str | None = None,
        user_id: str | None = None,
    ):

        query = (
            db.query(Expense)
            .options(
                joinedload(Expense.submitted_by_user),
                joinedload(Expense.category),

                joinedload(Expense.approved_by_user),
                joinedload(Expense.rejected_by_user),
                joinedload(Expense.paid_by_user),
            )
        )

        if user_id:
            query = query.filter(
                Expense.user_id == user_id
            )

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
            query = query.join(Expense.submitted_by_user)

            query = query.filter(
                or_(
                    Expense.title.ilike(f"%{search}%"),
                    Expense.description.ilike(f"%{search}%"),
                    Expense.payment_method.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%"),
                    User.employee_id.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )
        if status:
            query = query.filter(
                Expense.status == ExpenseStatus(status)
            )

        return (
            query
            .order_by(Expense.expense_date.desc())
            .all()
        )
        
    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: str
    ):
        return (
            db.query(Expense)
            .filter(Expense.user_id == user_id)
            .options(
               joinedload(Expense.submitted_by_user),
               joinedload(Expense.category),

                joinedload(Expense.approved_by_user),
                joinedload(Expense.rejected_by_user),
                joinedload(Expense.paid_by_user),
            )
           .order_by(Expense.expense_date.desc())
           .all()
        )


    @staticmethod
    def get_by_status(
        db: Session,
        status: ExpenseStatus
):
        return (
    db.query(Expense)
    .filter(Expense.status == status)
    .options(
        joinedload(Expense.submitted_by_user),
        joinedload(Expense.category),

        joinedload(Expense.approved_by_user),
        joinedload(Expense.rejected_by_user),
        joinedload(Expense.paid_by_user),
    )
    .all()
)

    @staticmethod
    def get_by_status_list(
        db: Session,
        statuses: list[ExpenseStatus]
    ):
        return (
            db.query(Expense)
            .filter(Expense.status.in_(statuses))
            .options(
                joinedload(Expense.submitted_by_user),
                joinedload(Expense.category),

                joinedload(Expense.approved_by_user),
                joinedload(Expense.rejected_by_user),
                joinedload(Expense.paid_by_user),
             )
            .order_by(Expense.expense_date.desc())
            .all()
        )


    @staticmethod
    def get_paid_expenses(db: Session):
        return (
           db.query(Expense)
           .options(
    joinedload(Expense.submitted_by_user),
    joinedload(Expense.approved_by_user),
    joinedload(Expense.rejected_by_user),
    joinedload(Expense.paid_by_user),
)
            .filter(
            Expense.status == ExpenseStatus.PAID
            )
            .all()
    )