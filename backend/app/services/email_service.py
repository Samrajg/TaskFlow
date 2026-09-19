from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_password_reset_email(to_email: str, reset_token: str):
    # This is where actual email provider integration would go (e.g. SendGrid, AWS SES)
    reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"
    
    # In a real app, use the email provider's API
    # For now, we simulate sending an email
    
    email_content = f"""
    TaskFlow

    Password Reset Request

    We received a request to reset the password for your TaskFlow account.
    Click the button below to create a new password.

    Reset Link: {reset_url}

    This link will expire in 1 hour.
    If you did not request a password reset, you can safely ignore this email.
    """
    
    logger.info(f"Sending email to {to_email}")
    logger.info(email_content)
    
    # Mock return
    return True
