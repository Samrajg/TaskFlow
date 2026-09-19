from fastapi import APIRouter, Depends
from app.api.auth import get_current_user
from app.database import get_db, Database
from app.services import dashboard_service

router = APIRouter()

@router.get("")
async def get_dashboard(current_user: dict = Depends(get_current_user), db: Database = Depends(get_db)):
    data = await dashboard_service.get_dashboard_data(current_user["id"], db)
    
    return {
        "user": current_user,
        **data
    }
