from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
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

        body = f"""
Hello {username},

Welcome to HigherEd Portal.

Your account has been created successfully.

Username:
{username}

Email:
{email}

Temporary Password:
{temp_password}

Please log in and change your password immediately.

Regards,
HigherEd BPO Expense Tracker
"""

        message = MessageSchema(
            subject="Welcome to HigherEd Portal",
            recipients=[email],
            body=body,
            subtype="plain",
        )

        fm = FastMail(conf)

        await fm.send_message(message)