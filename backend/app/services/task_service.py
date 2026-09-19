import uuid
from datetime import datetime, timezone
from app.database import Database

async def _verify_category(user_id: str, category_id: str, db: Database) -> bool:
    if not category_id:
        return True
    res = await db.execute("SELECT id FROM categories WHERE id = ? AND user_id = ?", [category_id, user_id])
    return len(res) > 0

async def get_tasks(user_id: str, search: str, status: str, priority: str, category_id: str, due_date: str, sort_by: str, db: Database):
    query = """
        SELECT t.id, t.title, t.description, t.category_id, c.name as category_name, c.color as category_color,
               t.priority, t.status, t.due_date, t.due_time, t.completed_at, t.created_at, t.updated_at
        FROM tasks t
        LEFT JOIN categories c ON t.category_id = c.id AND c.user_id = ?
        WHERE t.user_id = ?
    """
    params = [user_id, user_id]
    
    if search:
        query += " AND (LOWER(t.title) LIKE LOWER(?) OR LOWER(COALESCE(t.description, '')) LIKE LOWER(?))"
        params.extend([f"%{search}%", f"%{search}%"])
    if status:
        query += " AND t.status = ?"
        params.append(status)
    if priority:
        query += " AND t.priority = ?"
        params.append(priority)
    if category_id:
        query += " AND t.category_id = ?"
        params.append(category_id)
        
    if due_date:
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        if due_date == "TODAY":
            query += " AND t.due_date = ?"
            params.append(today)
        elif due_date == "OVERDUE":
            query += " AND t.due_date < ? AND t.status NOT IN ('COMPLETED', 'CANCELLED')"
            params.append(today)
        elif due_date == "NONE":
            query += " AND t.due_date IS NULL"
    
    if sort_by == "PRIORITY":
        query += " ORDER BY CASE t.priority WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 WHEN 'LOW' THEN 3 ELSE 4 END ASC, t.created_at DESC"
    elif sort_by == "DUE_DATE":
        query += " ORDER BY t.due_date ASC NULLS LAST, t.due_time ASC NULLS LAST"
    else:
        query += " ORDER BY t.created_at DESC"
        
    return await db.execute(query, params)

async def create_task(user_id: str, task_data: dict, db: Database):
    if not await _verify_category(user_id, task_data.get("category_id"), db):
        raise ValueError("Invalid category_id")

    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    query = """
        INSERT INTO tasks (id, user_id, category_id, title, description, priority, status, due_date, due_time, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    await db.execute_write(query, [
        task_id, user_id, task_data.get("category_id"), task_data.get("title"), task_data.get("description"),
        task_data.get("priority", "MEDIUM"), task_data.get("status", "PENDING"), task_data.get("due_date"), task_data.get("due_time"),
        now, now
    ])
    
    log_id = str(uuid.uuid4())
    log_query = "INSERT INTO activity_logs (id, user_id, task_id, action, description, created_at) VALUES (?, ?, ?, ?, ?, ?)"
    await db.execute_write(log_query, [log_id, user_id, task_id, "CREATED", f'Created task "{task_data.get("title")}"', now])
    
    return task_id

async def update_task(user_id: str, task_id: str, task_data: dict, db: Database):
    if "category_id" in task_data and task_data["category_id"]:
        if not await _verify_category(user_id, task_data["category_id"], db):
            raise ValueError("Invalid category_id")

    # Fetch previous state
    prev = await db.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", [task_id, user_id])
    if not prev:
        return False
    prev_task = prev[0]
    
    updates = []
    params = []
    now = datetime.now(timezone.utc).isoformat()
    logs = []
    
    for key, value in task_data.items():
        if value != prev_task.get(key) and value is not None:
            updates.append(f"{key} = ?")
            params.append(value)
            
            # Identify specific logs
            if key == "status":
                logs.append(("STATUS_CHANGED", f'Changed status to {value}'))
            elif key == "priority":
                logs.append(("PRIORITY_CHANGED", f'Changed priority from {prev_task.get("priority")} to {value}'))
            elif key == "category_id":
                logs.append(("CATEGORY_CHANGED", 'Changed task category'))
    
    if not updates:
        return True
        
    if "status" in task_data and task_data["status"] == "COMPLETED" and prev_task.get("status") != "COMPLETED":
        updates.append("completed_at = ?")
        params.append(now)
        logs.append(("COMPLETED", f'Completed task "{prev_task.get("title")}"'))
        
    updates.append("updated_at = ?")
    params.append(now)
    params.append(task_id)
    params.append(user_id)
    
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
    await db.execute_write(query, params)
    
    # If it was just a generic update not caught by specific fields
    if not logs:
        logs.append(("UPDATED", f'Updated task "{prev_task.get("title")}"'))
        
    for action, desc in logs:
        log_id = str(uuid.uuid4())
        log_query = "INSERT INTO activity_logs (id, user_id, task_id, action, description, created_at) VALUES (?, ?, ?, ?, ?, ?)"
        await db.execute_write(log_query, [log_id, user_id, task_id, action, desc, now])
    
    return True

async def delete_task(user_id: str, task_id: str, db: Database):
    prev = await db.execute("SELECT title FROM tasks WHERE id = ? AND user_id = ?", [task_id, user_id])
    if not prev:
        return False
    title = prev[0]["title"]
    
    now = datetime.now(timezone.utc).isoformat()
    log_id = str(uuid.uuid4())
    log_query = "INSERT INTO activity_logs (id, user_id, task_id, action, description, created_at) VALUES (?, ?, ?, ?, ?, ?)"
    await db.execute_write(log_query, [log_id, user_id, None, "DELETED", f'Deleted task "{title}"', now])
    
    await db.execute_write("DELETE FROM tasks WHERE id = ? AND user_id = ?", [task_id, user_id])
    return True
