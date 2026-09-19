from app.database import Database

async def get_categories(user_id: str, db: Database):
    query = "SELECT id, name, color, icon, created_at, updated_at FROM categories WHERE user_id = ? ORDER BY name ASC"
    return await db.execute(query, [user_id])
