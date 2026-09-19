import uuid
from datetime import datetime, timezone
from app.database import Database

async def create_task(user_id: str, task_data: dict, db: Database):
    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    query = """
        INSERT INTO tasks (id, user_id, category_id, title, description, priority, status, due_date, due_time, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    await db.execute_write(query, [
        task_id, user_id, task_data.get("category_id"), task_data.get("title"), task_data.get("description"),
        task_data.get("priority", "MEDIUM"), "PENDING", task_data.get("due_date"), task_data.get("due_time"),
        now, now
    ])
    
    # Activity log
    log_id = str(uuid.uuid4())
    log_query = "INSERT INTO activity_logs (id, user_id, task_id, action, created_at) VALUES (?, ?, ?, ?, ?)"
    await db.execute_write(log_query, [log_id, user_id, task_id, "CREATED", now])
    
    return task_id

async def update_task(user_id: str, task_id: str, task_data: dict, db: Database):
    updates = []
    params = []
    now = datetime.now(timezone.utc).isoformat()
    
    for key, value in task_data.items():
        if value is not None:
            updates.append(f"{key} = ?")
            params.append(value)
            
    if not updates:
        return True
        
    if "status" in task_data and task_data["status"] == "COMPLETED":
        updates.append("completed_at = ?")
        params.append(now)
        
    updates.append("updated_at = ?")
    params.append(now)
    
    params.append(task_id)
    params.append(user_id)
    
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
    await db.execute_write(query, params)
    
    # Activity log
    action = "COMPLETED" if task_data.get("status") == "COMPLETED" else "UPDATED"
    log_id = str(uuid.uuid4())
    log_query = "INSERT INTO activity_logs (id, user_id, task_id, action, created_at) VALUES (?, ?, ?, ?, ?)"
    await db.execute_write(log_query, [log_id, user_id, task_id, action, now])
    
    return True
