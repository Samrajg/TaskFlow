from datetime import datetime, timedelta, timezone
from app.database import Database

async def get_dashboard_data(user_id: str, db: Database):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    # Summary
    summary_query = """
        SELECT 
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_tasks,
            SUM(CASE WHEN status IN ('PENDING', 'IN_PROGRESS') THEN 1 ELSE 0 END) as pending_tasks,
            SUM(CASE WHEN due_date < ? AND status NOT IN ('COMPLETED', 'CANCELLED') THEN 1 ELSE 0 END) as overdue_tasks
        FROM tasks
        WHERE user_id = ?
    """
    summary_res = await db.execute(summary_query, [today, user_id])
    summary = summary_res[0] if summary_res else {"total_tasks":0, "completed_tasks":0, "pending_tasks":0, "overdue_tasks":0}
    
    # Ensure no None values
    for k in summary:
        if summary[k] is None: summary[k] = 0

    # Today's Progress
    today_query = """
        SELECT 
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_tasks
        FROM tasks
        WHERE user_id = ? AND due_date = ?
    """
    today_res = await db.execute(today_query, [user_id, today])
    today_stats = today_res[0] if today_res else {"total_tasks":0, "completed_tasks":0}
    if today_stats["total_tasks"] is None: today_stats["total_tasks"] = 0
    if today_stats["completed_tasks"] is None: today_stats["completed_tasks"] = 0
    progress_percentage = (today_stats["completed_tasks"] / today_stats["total_tasks"] * 100) if today_stats["total_tasks"] > 0 else 0

    # Today's Tasks
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
    today_tasks = await db.execute(today_tasks_query, [user_id, today])

    # Status Distribution
    status_query = """
        SELECT status, COUNT(*) as count
        FROM tasks
        WHERE user_id = ?
        GROUP BY status
    """
    status_dist = await db.execute(status_query, [user_id])

    # Category Distribution
    cat_query = """
        SELECT c.id as category_id, c.name as category_name, c.color, COUNT(t.id) as count
        FROM categories c
        LEFT JOIN tasks t ON t.category_id = c.id AND t.user_id = ?
        WHERE c.user_id = ?
        GROUP BY c.id, c.name, c.color
        ORDER BY count DESC
    """
    cat_dist = await db.execute(cat_query, [user_id, user_id])

    # Recent Activity
    activity_query = """
        SELECT a.id, a.action, a.created_at, t.title as task_title
        FROM activity_logs a
        LEFT JOIN tasks t ON a.task_id = t.id
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
        LIMIT 10
    """
    recent_activity = await db.execute(activity_query, [user_id])
    
    # Weekly Productivity
    weekly = []
    for i in range(6, -1, -1):
        date_obj = datetime.now(timezone.utc) - timedelta(days=i)
        date_str = date_obj.strftime('%Y-%m-%d')
        day_str = date_obj.strftime('%A')
        
        day_q = """
            SELECT 
                COUNT(*) as created,
                SUM(CASE WHEN status = 'COMPLETED' AND date(completed_at) = ? THEN 1 ELSE 0 END) as completed
            FROM tasks
            WHERE user_id = ? AND date(created_at) = ?
        """
        # Actually a better query for created vs completed on a specific day
        # Created on that day
        created_q = "SELECT COUNT(*) as c FROM tasks WHERE user_id = ? AND date(created_at) = ?"
        cr_res = await db.execute(created_q, [user_id, date_str])
        cr_count = cr_res[0]["c"] if cr_res else 0
        
        # Completed on that day
        comp_q = "SELECT COUNT(*) as c FROM activity_logs WHERE user_id = ? AND action = 'COMPLETED' AND date(created_at) = ?"
        co_res = await db.execute(comp_q, [user_id, date_str])
        co_count = co_res[0]["c"] if co_res else 0
        
        weekly.append({
            "date": date_str,
            "day": day_str,
            "created": cr_count,
            "completed": co_count
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
