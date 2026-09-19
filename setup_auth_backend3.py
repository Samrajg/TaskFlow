import os

service_email = """from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_password_reset_email(to_email: str, reset_token: str):
    # This is where actual email provider integration would go (e.g. SendGrid, AWS SES)
    reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"
    
    # In a real app, use the email provider's API
    # For now, we simulate sending an email
    
    email_content = f\"\"\"
    TaskFlow

    Password Reset Request

    We received a request to reset the password for your TaskFlow account.
    Click the button below to create a new password.

    Reset Link: {reset_url}

    This link will expire in 1 hour.
    If you did not request a password reset, you can safely ignore this email.
    \"\"\"
    
    logger.info(f"Sending email to {to_email}")
    logger.info(email_content)
    
    # Mock return
    return True
"""
with open("backend/app/services/email_service.py", "w") as f: f.write(service_email)

service_auth = """import uuid
from app.database import get_db
from app.utils.password import verify_password, get_password_hash
from app.utils.tokens import generate_reset_token, hash_token, get_token_expiration
from app.services.email_service import send_password_reset_email
from datetime import datetime, timezone

async def login(email: str, password: str, db):
    query = "SELECT * FROM users WHERE email = ?"
    results = await db.execute(query, [email])
    
    if not results:
        return None
    
    user = results[0]
    if not verify_password(password, user["password_hash"]):
        return None
    
    return user

async def request_password_reset(email: str, db):
    # Find user
    query = "SELECT id FROM users WHERE email = ?"
    results = await db.execute(query, [email])
    if not results:
        return True # Return true even if not found to prevent enumeration
    
    user_id = results[0]["id"]
    
    raw_token = generate_reset_token()
    hashed_token = hash_token(raw_token)
    expires_at = get_token_expiration(hours=1)
    
    # Insert token
    token_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    
    insert_query = \"\"\"
        INSERT INTO password_reset_tokens (id, user_id, token_hash, expires_at, created_at)
        VALUES (?, ?, ?, ?, ?)
    \"\"\"
    await db.execute_write(insert_query, [token_id, user_id, hashed_token, expires_at, created_at])
    
    # Send email
    await send_password_reset_email(email, raw_token)
    
    return True

async def reset_password(token: str, new_password: str, db):
    hashed_token = hash_token(token)
    
    # Find token
    query = "SELECT * FROM password_reset_tokens WHERE token_hash = ?"
    results = await db.execute(query, [hashed_token])
    
    if not results:
        return False
        
    token_record = results[0]
    
    # Check if used
    if token_record["used_at"] is not None:
        return False
        
    # Check expiration
    expires_at = datetime.fromisoformat(token_record["expires_at"].replace('Z', '+00:00'))
    if datetime.now(timezone.utc) > expires_at:
        return False
        
    # Hash new password
    new_password_hash = get_password_hash(new_password)
    user_id = token_record["user_id"]
    
    # Update user password
    update_pwd_query = "UPDATE users SET password_hash = ? WHERE id = ?"
    await db.execute_write(update_pwd_query, [new_password_hash, user_id])
    
    # Mark token used
    used_at = datetime.now(timezone.utc).isoformat()
    update_token_query = "UPDATE password_reset_tokens SET used_at = ? WHERE id = ?"
    await db.execute_write(update_token_query, [used_at, token_record["id"]])
    
    return True
"""
with open("backend/app/services/auth_service.py", "w") as f: f.write(service_auth)

api_auth = """from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.services import auth_service
from app.database import get_db, Database

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest, db: Database = Depends(get_db)):
    user = await auth_service.login(request.email, request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    
    # Return user details without password hash
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "message": "Login successful"
    }

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Database = Depends(get_db)):
    await auth_service.request_password_reset(request.email, db)
    return {"message": "If an account exists for this email, a password reset link has been sent."}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Database = Depends(get_db)):
    success = await auth_service.reset_password(request.token, request.new_password, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token."
        )
    return {"message": "Password updated successfully."}
"""
with open("backend/app/api/auth.py", "w") as f: f.write(api_auth)
