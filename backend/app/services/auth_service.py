import uuid
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
    
    insert_query = """
        INSERT INTO password_reset_tokens (id, user_id, token_hash, expires_at, created_at)
        VALUES (?, ?, ?, ?, ?)
    """
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
