import asyncio
from app.database import Database
from app.utils.password import get_password_hash
async def update():
    db = Database()
    hash_str = get_password_hash("password123")
    await db.execute_write('UPDATE users SET password_hash = ? WHERE id = ?', [hash_str, 'usr_test'])
asyncio.run(update())
