from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.user import User

from app.repositories.expense_repository import ExpenseRepository
from app.repositories.category_repository import CategoryRepository

from app.schemas.expense import ExpenseCreate
from app.schemas.expense import ExpenseUpdate

from app.schemas.expense import ExpenseUpdate

from datetime import date

from app.core.permissions import is_admin
from app.models.expense import Expense

from app.models.enums import ExpenseStatus
from app.core.permissions import is_admin_or_manager

import csv
from io import StringIO

import os
import shutil
import uuid
from datetime import datetime

from app.models.enums import UserRole

from app.schemas.user import UserResponse
from app.models.company import Company
from app.models.department import Department
from fastapi import BackgroundTasks
from app.services.email_service import EmailService

class ExpenseService:


    @staticmethod
    def create(
        db: Session,
        title: str,
        description: str | None,
        amount: float,
        expense_date: date,
        payment_method: str,
        category_id: str,
        receipt_path: str | None,
        current_user: User,
        ):

        category = CategoryRepository.get_by_id(
               db,
               category_id
            )

        if not category:
            raise ValueError("Category not found")

        expense = Expense(
            title=title,
            description=description,
            amount=amount,
            expense_date=expense_date,
            payment_method=payment_method,
            category_id=category_id,
            receipt_path=receipt_path,
            user_id=current_user.id,
        )

        created_expense = ExpenseRepository.create(
             db,
             expense
            )


        return created_expense
    
    @staticmethod
    def get_all(
        db: Session,
        current_user: User
    ):

        role = str(current_user.role).upper()

    # Admin -> All expenses
        if role == "ADMIN":

            expenses = ExpenseRepository.get_all(db)

    # Manager -> Only submitted expenses
        elif role == "MANAGER":

            expenses = ExpenseRepository.get_by_status(
                db,
                ExpenseStatus.SUBMITTED
            )

    # Finance -> Approved + Paid
        elif role == "FINANCE":

            expenses = ExpenseRepository.get_by_status_list(
                db,
                [
                ExpenseStatus.APPROVED
                ]
            )

    # Employee -> Own expenses
        else:

            expenses = ExpenseRepository.get_by_user_id(
                db,
                current_user.id
             )

        return expenses

    @staticmethod
    def get_by_id(
        db: Session,
        expense_id: str,
        current_user: User
):

        expense = ExpenseRepository.get_by_id(
            db,
            expense_id
    )

        if not expense:
            raise ValueError(
               "Expense not found"
        )

        ExpenseService.validate_expense_access(
            expense,
            current_user
        )

        expense.approved_by_name = (
            expense.approved_by_user.username
            if expense.approved_by_user
            else None
        )

        expense.rejected_by_name = (
            expense.rejected_by_user.username
            if expense.rejected_by_user
            else None
         )

        return expense

    @staticmethod
    def delete(
        db: Session,
        expense_id: str,
        current_user: User
    ):
        expense = ExpenseRepository.get_by_id(
            db,
            expense_id
        )

        if not expense:
            raise ValueError(
                "Expense not found"
            )

        if current_user.role != UserRole.EMPLOYEE:
            raise ValueError("Only employees can delete expenses")

        ExpenseService.validate_expense_access(
            expense,
            current_user
        )

        ExpenseRepository.delete(
            db,
            expense
        )

    @staticmethod
    def update(
       db: Session,
       expense_id: str,
       title: str,
       description: str | None,
       amount: float,
       expense_date: date,
       payment_method: str,
       category_id: str,
       receipt_path: str | None,
       current_user: User
):
        expense = ExpenseRepository.get_by_id(
           db,
           expense_id
         )

        if not expense:
            raise ValueError("Expense not found")

        if current_user.role != UserRole.EMPLOYEE:
            raise ValueError("Only employees can edit expenses")

        ExpenseService.validate_expense_access(
            expense,
            current_user
        )

        category = CategoryRepository.get_by_id(
            db,
            category_id
        )

        if not category:
           raise ValueError("Category not found")

        expense.title = title
        expense.description = description
        expense.amount = amount
        expense.expense_date = expense_date
        expense.payment_method = payment_method
        expense.category_id = category_id

   # Update receipt only if a new file was uploaded
        if receipt_path:

    # Delete old receipt if it exists
            if (
                expense.receipt_path
                and os.path.exists(expense.receipt_path)
            ):
                os.remove(expense.receipt_path)

            expense.receipt_path = receipt_path

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
        search: str | None = None,
        status: str | None = None,
        current_user: User = None,
        
    ):

    # Admin & Manager
        if is_admin_or_manager(current_user):
            return ExpenseRepository.filter_expenses(
                db=db,
                category_id=category_id,
                payment_method=payment_method,
                start_date=start_date,
                end_date=end_date,
                search=search,
                status=status,
            )

        
    # Finance
        if current_user.role.upper() == "FINANCE":
            
            return ExpenseRepository.filter_expenses(
                db=db,
                category_id=category_id,
                payment_method=payment_method,
                start_date=start_date,
                end_date=end_date,
                search=search,
                status=status,
            )

        
    # Employee
        return ExpenseRepository.filter_expenses(
            db=db,
            category_id=category_id,
            payment_method=payment_method,
            start_date=start_date,
            end_date=end_date,
            search=search,
            status=status,
            user_id=current_user.id,
        )

    @staticmethod
    def export_csv(
        db: Session,
        category: str | None = None,
        payment_method: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        search: str | None = None,
    ):
        expenses = ExpenseRepository.filter_expenses(
            db=db,
            category_id=category,
            payment_method=payment_method,
            start_date=from_date,
            end_date=to_date,
            search=search,
        )

        output = StringIO()

        writer = csv.writer(output)

        writer.writerow([
            "Title",
            "Description",
            "Amount",
            "Payment Method",
            "Expense Date",
        ])

        for expense in expenses:
            writer.writerow([
               expense.title,
               expense.description,
               expense.amount,
               expense.payment_method,
               expense.expense_date,
            ])

        return output.getvalue()

    @staticmethod
    def validate_expense_access(
    expense: Expense,
    current_user: User
    ):
        if is_admin(current_user):
            return

        if expense.user_id != current_user.id:
            raise ValueError(
               "Access denied"
        )

    @staticmethod
    def approve_expense(
        db: Session,
        expense_id: str,
        current_user: User,
        background_tasks: BackgroundTasks,
    ):
        if current_user.role != UserRole.MANAGER:
            raise ValueError("Manager access required")

        expense = ExpenseRepository.get_by_id(
             db,
             expense_id
        )

        if not expense:
            raise ValueError("Expense not found")

        if expense.status != ExpenseStatus.SUBMITTED:
            raise ValueError("Expense already processed")

        expense.status = ExpenseStatus.APPROVED
        expense.approved_by = current_user.id
        expense.approved_at = datetime.utcnow()

        updated_expense = ExpenseRepository.update(
            db,
            expense
        )

    # Send email in background
        background_tasks.add_task(
           EmailService.send_manager_approved_email,
           email=updated_expense.submitted_by_user.email,
           username=updated_expense.submitted_by_user.username,
           title=updated_expense.title,
           category=updated_expense.category_name,
           amount=float(updated_expense.amount),
           expense_date=str(updated_expense.expense_date),
           payment_method=updated_expense.payment_method,
        )

        return updated_expense

    @staticmethod
    def reject_expense(
        db: Session,
        expense_id: str,
        current_user: User,
        rejection_reason: str,
        background_tasks: BackgroundTasks,
    ):
        if current_user.role != UserRole.MANAGER:
            raise ValueError("Manager access required")

        expense = ExpenseRepository.get_by_id(
            db,
            expense_id
        )

        if not expense:
            raise ValueError("Expense not found")

        if expense.status != ExpenseStatus.SUBMITTED:
            raise ValueError("Expense already processed")

        expense.status = ExpenseStatus.REJECTED
        expense.rejected_by = current_user.id
        expense.rejected_at = datetime.utcnow()
        expense.rejection_reason = rejection_reason

        updated_expense = ExpenseRepository.update(
            db,
            expense
        )

        background_tasks.add_task(
            EmailService.send_manager_rejected_email,
            email=updated_expense.submitted_by_user.email,
            username=updated_expense.submitted_by_user.username,
            title=updated_expense.title,
            category=updated_expense.category_name,
            amount=float(updated_expense.amount),
            expense_date=str(updated_expense.expense_date),
            payment_method=updated_expense.payment_method,
            rejection_reason=updated_expense.rejection_reason,
            manager=current_user.username,
        )

        return updated_expense

    @staticmethod
    def mark_as_paid(
        db: Session,
        expense_id: str,
        payment_reference: str,
        payment_notes: str | None,
        current_user: User,
        background_tasks: BackgroundTasks,
    ):
        if current_user.role != UserRole.FINANCE:
            raise ValueError("Finance access required")

        expense = ExpenseRepository.get_by_id(
            db,
            expense_id
        )

        if not expense:
            raise ValueError("Expense not found")

        if expense.status != ExpenseStatus.APPROVED:
            raise ValueError(
               "Only approved expenses can be paid"
        )

        expense.status = ExpenseStatus.PAID

        expense.paid_by = current_user.id
        expense.paid_at = datetime.utcnow()
        expense.payment_reference = payment_reference
        expense.payment_notes = payment_notes

        updated_expense = ExpenseRepository.update(
            db,
           expense
         )

        background_tasks.add_task(
            EmailService.send_finance_paid_email,
            email=updated_expense.submitted_by_user.email,
            username=updated_expense.submitted_by_user.username,
            title=updated_expense.title,
            category=updated_expense.category_name,
            amount=float(updated_expense.amount),
            expense_date=str(updated_expense.expense_date),
            payment_method=updated_expense.payment_method,
            payment_reference=updated_expense.payment_reference,
            finance=current_user.username,
        )

        return updated_expense


    @staticmethod
    def get_paid_expenses(
        db: Session,
        search: str | None = None,
    ):
        return ExpenseRepository.get_paid_expenses(
        db,
        search=search,
    )