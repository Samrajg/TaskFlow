import asyncio
from datetime import datetime, timedelta, timezone
from app.database import Database

async def get_dashboard_data(user_id: str, db: Database):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=6)).strftime('%Y-%m-%d')
    
    summary_query = """
        SELECT 
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_tasks,
            SUM(CASE WHEN status IN ('PENDING', 'IN_PROGRESS') THEN 1 ELSE 0 END) as pending_tasks,
            SUM(CASE WHEN due_date < ? AND status NOT IN ('COMPLETED', 'CANCELLED') THEN 1 ELSE 0 END) as overdue_tasks
        FROM tasks
        WHERE user_id = ?
    """
    
    today_query = """
        SELECT 
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_tasks
        FROM tasks
        WHERE user_id = ? AND due_date = ?
    """
    
    today_tasks_query = """
        SELECT t.id, t.title, t.priority, t.status, t.due_time, c.name as category_name, c.color as category_color
        FROM tasks t
        LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? AND t.due_date = ?
        ORDER BY 
            CASE t.status
                WHEN 'IN_PROGRESS' THEN 1
                WHEN 'PENDING' THEN 2
                WHEN 'COMPLETED' THEN 3
                ELSE 4
            END, t.due_time
    """
    
    status_query = """
        SELECT status, COUNT(*) as count
        FROM tasks
        WHERE user_id = ?
        GROUP BY status
    """
    
    cat_query = """
        SELECT c.id as category_id, c.name as category_name, c.color, COUNT(t.id) as count
        FROM categories c
        LEFT JOIN tasks t ON t.category_id = c.id AND t.user_id = ?
        WHERE c.user_id = ?
        GROUP BY c.id, c.name, c.color
        ORDER BY count DESC
    """
    
    activity_query = """
        SELECT a.id, a.action, a.created_at, t.title as task_title
        FROM activity_logs a
        LEFT JOIN tasks t ON a.task_id = t.id
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
        LIMIT 10
    """
    
    created_q = "SELECT date(created_at) as d, COUNT(*) as c FROM tasks WHERE user_id = ? AND date(created_at) >= ? GROUP BY date(created_at)"
    comp_q = "SELECT date(created_at) as d, COUNT(*) as c FROM activity_logs WHERE user_id = ? AND action = 'COMPLETED' AND date(created_at) >= ? GROUP BY date(created_at)"

    # Execute all 8 queries concurrently
    results = await asyncio.gather(
        db.execute(summary_query, [today, user_id]),
        db.execute(today_query, [user_id, today]),
        db.execute(today_tasks_query, [user_id, today]),
        db.execute(status_query, [user_id]),
        db.execute(cat_query, [user_id, user_id]),
        db.execute(activity_query, [user_id]),
        db.execute(created_q, [user_id, seven_days_ago]),
        db.execute(comp_q, [user_id, seven_days_ago])
    )
    
    summary_res, today_res, today_tasks, status_dist, cat_dist, recent_activity, cr_res, co_res = results

    summary = summary_res[0] if summary_res else {"total_tasks":0, "completed_tasks":0, "pending_tasks":0, "overdue_tasks":0}
    for k in summary:
        if summary[k] is None: summary[k] = 0

    today_stats = today_res[0] if today_res else {"total_tasks":0, "completed_tasks":0}
    if today_stats["total_tasks"] is None: today_stats["total_tasks"] = 0
    if today_stats["completed_tasks"] is None: today_stats["completed_tasks"] = 0
    progress_percentage = (today_stats["completed_tasks"] / today_stats["total_tasks"] * 100) if today_stats["total_tasks"] > 0 else 0

    cr_map = {r["d"]: r["c"] for r in cr_res} if cr_res else {}
    co_map = {r["d"]: r["c"] for r in co_res} if co_res else {}
    
    weekly = []
    for i in range(6, -1, -1):
        date_obj = datetime.now(timezone.utc) - timedelta(days=i)
        date_str = date_obj.strftime('%Y-%m-%d')
        day_str = date_obj.strftime('%A')
        weekly.append({
            "date": date_str,
            "day": day_str,
            "created": cr_map.get(date_str, 0),
            "completed": co_map.get(date_str, 0)
        })

    return {
        "summary": summary,
        "today": {
            "date": today,
            "total_tasks": today_stats["total_tasks"],
            "completed_tasks": today_stats["completed_tasks"],
            "progress_percentage": round(progress_percentage)
        },
        "today_tasks": today_tasks,
        "status_distribution": status_dist,
        "category_distribution": cat_dist,
        "recent_activity": recent_activity,
        "weekly_productivity": weekly
    }
