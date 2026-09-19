import asyncio
from app.database import Database
async def update():
    db = Database()
    hash_str = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQGjZ3mC"
    await db.execute_write('UPDATE users SET password_hash = ? WHERE id = ?', [hash_str, 'usr_test'])
asyncio.run(update())
