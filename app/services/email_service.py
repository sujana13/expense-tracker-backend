from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings

import logging

logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class EmailService:

    @staticmethod
    async def send_welcome_email(
        email: EmailStr,
        username: str,
        temp_password: str,
    ):
        logger.info("📧 Starting welcome email...")
        logger.info(f"Recipient: {email}")

        body = f"""
Hello {username},

Welcome to HigherEd Portal.

Your account has been created successfully.

Username: {username}
Email: {email}

Temporary Password: {temp_password}

Please log in and change your password immediately.
"""

        message = MessageSchema(
            subject="Welcome to HigherEd Portal",
            recipients=[email],
            body=body,
            subtype="plain",
        )

        fm = FastMail(conf)

        try:
            await fm.send_message(message)
            logger.info("✅ Welcome email sent successfully!")
        except Exception as e:
            logger.exception(f"❌ Email failed: {e}")


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

        message = MessageSchema(
            subject="Expense Submitted Successfully",
            recipients=[email],
            body=body,
            subtype="plain",
        )

        fm = FastMail(conf)

        await fm.send_message(message)

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

        message = MessageSchema(
            subject="Expense Approved by Manager",
            recipients=[email],
            body=body,
            subtype="plain",
        )

        fm = FastMail(conf)

        await fm.send_message(message)

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

        message = MessageSchema(
            subject="Expense Rejected by Manager",
            recipients=[email],
            body=body,
            subtype="plain",
        )

        fm = FastMail(conf)

        await fm.send_message(message)

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

        message = MessageSchema(
            subject="Expense Payment Completed",
            recipients=[email],
            body=body,
            subtype="plain",
        )

        fm = FastMail(conf)

        await fm.send_message(message)
