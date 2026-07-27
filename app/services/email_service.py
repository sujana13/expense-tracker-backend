from pydantic import EmailStr
from app.core.config import settings

import resend

resend.api_key = settings.RESEND_API_KEY



class EmailService:

    @staticmethod
    async def send_welcome_email(
        email: EmailStr,
        username: str,
        temp_password: str,
    ):

        body = f"""
Hello {username},

Welcome to HigherEd Portal.

Your account has been created successfully.

Username: {username}
Email: {email}

Temporary Password: {temp_password}

Please log in and change your password immediately.
"""

        resend.Emails.send(
        {
        "from": "Expense Tracker <onboarding@resend.dev>",
        "to": [email],
        "subject": "Welcome to HigherEd Portal",
        "text": body,
    }
)


    @staticmethod
    async def send_expense_created_email(
        email: EmailStr,
        username: str,
        title: str,
        category: str,
        amount: float,
        expense_date: str,
        payment_method: str,
        status: str,
    ):

        body = f"""
Hello {username},

Your expense has been submitted successfully.

Expense Details
-------------------------------
Title          : {title}
Category       : {category}
Amount         : ₹{amount:.2f}
Expense Date   : {expense_date}
Payment Method : {payment_method}
Status         : {status}

Thank you,

HigherEd Portal
"""

        resend.Emails.send(
    {
        "from": "Expense Tracker <onboarding@resend.dev>",
        "to": [email],
        "subject": "Expense Submitted Successfully",
        "text": body,
    }
)

    @staticmethod
    async def send_manager_approved_email(
        email: EmailStr,
        username: str,
        title: str,
        category: str,
        amount: float,
        expense_date: str,
        payment_method: str,
    ):
        body = f"""
Hello {username},

Good news!

Your expense has been approved by your Manager.

Expense Details

Title:
{title}

Category:
{category}

Amount:
₹{amount}

Expense Date:
{expense_date}

Payment Method:
{payment_method}

Status:
Manager Approved

Your expense has now been forwarded to the Finance Team for final approval.

Regards,
HigherEd Portal
"""

        resend.Emails.send(
    {
        "from": "Expense Tracker <onboarding@resend.dev>",
        "to": [email],
        "subject": "Expense Approved by Manager",
        "text": body,
    }
)

    @staticmethod
    async def send_manager_rejected_email(
        email: str,
        username: str,
        title: str,
        category: str,
        amount: float,
        expense_date: str,
        payment_method: str,
        rejection_reason: str,
        manager: str,
    ):

        body = f"""
Hello {username},

Your expense request has been reviewed and has been rejected by your manager.

Expense Details
----------------------------------------
Title: {title}
Category: {category}
Amount: ₹{amount}
Expense Date: {expense_date}
Payment Method: {payment_method}

Rejected By:
{manager}

Reason:
{rejection_reason}

Please review the comments, make the necessary corrections, and submit the expense again if applicable.

Regards,
HigherEd Portal
"""

        resend.Emails.send(
    {
        "from": "Expense Tracker <onboarding@resend.dev>",
        "to": [email],
        "subject": "Expense Rejected by Manager",
        "text": body,
    }
)
    @staticmethod
    async def send_finance_paid_email(
        email: str,
        username: str,
        title: str,
        category: str,
        amount: float,
        expense_date: str,
        payment_method: str,
        payment_reference: str,
        finance: str,
    ):

        body = f"""
Hello {username},
Good news! 

Your expense has been processed and paid by the Finance Team.

=========================================
Expense Details
=========================================

Title            : {title}
Category         : {category}
Amount           : ₹{amount}
Expense Date     : {expense_date}
Payment Method   : {payment_method}

=========================================
Payment Details
=========================================

Payment Reference : {payment_reference}
Processed By      : {finance}

Your reimbursement has been completed successfully.


Regards,
Finance Team
"""

        resend.Emails.send(
    {
        "from": "Expense Tracker <onboarding@resend.dev>",
        "to": [email],
        "subject": "Expense Payment Completed",
        "text": body,
    }
)
