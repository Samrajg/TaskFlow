from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.api.auth import get_current_user
from app.database import get_db, Database
from app.services import task_service

router = APIRouter()

@router.get("")
async def get_tasks(
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category_id: Optional[str] = None,
    due_date: Optional[str] = None,
    sort_by: Optional[str] = "NEWEST",
    current_user: dict = Depends(get_current_user), 
    db: Database = Depends(get_db)
):
    tasks = await task_service.get_tasks(
        current_user["id"], search, status, priority, category_id, due_date, sort_by, db
    )
    return {"items": tasks, "total": len(tasks)}

@router.post("")
async def create_task(request: TaskCreate, current_user: dict = Depends(get_current_user), db: Database = Depends(get_db)):
    try:
        task_id = await task_service.create_task(current_user["id"], request.model_dump(), db)
        return {"id": task_id, "message": "Task created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.patch("/{task_id}")
async def update_task(task_id: str, request: TaskUpdate, current_user: dict = Depends(get_current_user), db: Database = Depends(get_db)):
    try:
        success = await task_service.update_task(current_user["id"], task_id, request.model_dump(exclude_unset=True), db)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.delete("/{task_id}")
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user), db: Database = Depends(get_db)):
    success = await task_service.delete_task(current_user["id"], task_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
