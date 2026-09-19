from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.services import auth_service
from app.database import get_db, Database

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest, db: Database = Depends(get_db)):
    user = await auth_service.login(request.email, request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    
    # Return user details without password hash
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "message": "Login successful"
    }

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Database = Depends(get_db)):
    await auth_service.request_password_reset(request.email, db)
    return {"message": "If an account exists for this email, a password reset link has been sent."}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Database = Depends(get_db)):
    success = await auth_service.reset_password(request.token, request.new_password, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token."
        )
    return {"message": "Password updated successfully."}
