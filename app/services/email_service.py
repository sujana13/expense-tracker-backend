from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings

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

        print("===== SEND EMAIL FUNCTION CALLED =====")
        print("Recipient:", email)

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

        print("===== EMAIL SENT SUCCESSFULLY =====")