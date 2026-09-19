import secrets
import hashlib
from datetime import datetime, timedelta, timezone

def generate_reset_token():
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def get_token_expiration(hours=1):
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()
