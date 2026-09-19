from fastapi import APIRouter, Depends, HTTPException
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.api.auth import get_current_user
from app.database import get_db, Database
from app.services import task_service

router = APIRouter()

@router.post("")
async def create_task(request: TaskCreate, current_user: dict = Depends(get_current_user), db: Database = Depends(get_db)):
    task_id = await task_service.create_task(current_user["id"], request.model_dump(), db)
    return {"id": task_id, "message": "Task created successfully"}

@router.patch("/{task_id}")
async def update_task(task_id: str, request: TaskUpdate, current_user: dict = Depends(get_current_user), db: Database = Depends(get_db)):
    success = await task_service.update_task(current_user["id"], task_id, request.model_dump(exclude_unset=True), db)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update task")
    return {"message": "Task updated successfully"}
