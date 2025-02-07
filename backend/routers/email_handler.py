import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

# Configuration for FastMail with credentials from environment variables
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),  # Fetch from environment
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),  # Fetch from environment
    MAIL_FROM=os.getenv("MAIL_FROM"),  # Fetch from environment
    MAIL_PORT=587,  # Standard port for SMTP with STARTTLS
    MAIL_SERVER="smtp.gmail.com",  # Replace with your SMTP server
    MAIL_FROM_NAME="Your App Name",  # Custom "From" Name
    MAIL_STARTTLS=True,  # Enable STARTTLS encryption
    MAIL_SSL_TLS=False,  # Disable SSL/TLS (not needed with STARTTLS)
    USE_CREDENTIALS=True,  # Use the provided credentials
    VALIDATE_CERTS=True,  # Validate SSL certificates
)


async def send_reset_email(email: str, token: str):
    reset_link = f"http://127.0.0.1:8000/auth/reset_password/{token}"

    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],  # List of recipients
        body=f"Click on the link to reset your password: {reset_link}",
        subtype="html",
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
