import asyncio
import uuid
from datetime import datetime, timezone
from app.database import Database
from app.utils.password import get_password_hash

async def insert_user():
    db = Database()
    
    # User details
    user_id = str(uuid.uuid4())
    name = "godwin"
    email = "samrajgodwin7@gmail.com"
    password_plain = "sam1234"
    
    # Hash password
    password_hash = get_password_hash(password_plain)
    
    created_at = datetime.now(timezone.utc).isoformat()
    updated_at = created_at
    
    print(f"Inserting user {name} ({email})...")
    
    # Insert query
    query = """
    INSERT INTO users (id, name, email, password_hash, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    
    await db.execute_write(query, [user_id, name, email, password_hash, created_at, updated_at])
    print("User successfully inserted!")

if __name__ == "__main__":
    asyncio.run(insert_user())
