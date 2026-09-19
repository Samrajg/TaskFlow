from fastapi import APIRouter, Depends
from app.api.auth import get_current_user
from app.database import get_db, Database
from app.services import category_service

router = APIRouter()

@router.get("")
async def get_categories(current_user: dict = Depends(get_current_user), db: Database = Depends(get_db)):
    categories = await category_service.get_categories(current_user["id"], db)
    return {"items": categories}
