import os

utils_password = """from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
"""
with open("backend/app/utils/password.py", "w") as f: f.write(utils_password)

utils_tokens = """import secrets
import hashlib
from datetime import datetime, timedelta, timezone

def generate_reset_token():
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def get_token_expiration(hours=1):
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()
"""
with open("backend/app/utils/tokens.py", "w") as f: f.write(utils_tokens)

schema_auth = """from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
"""
with open("backend/app/schemas/auth.py", "w") as f: f.write(schema_auth)
