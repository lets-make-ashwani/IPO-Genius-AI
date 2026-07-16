from fastapi import APIRouter, Depends, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.shared.dependencies import get_current_user
from app.modules.users.models.user import User
from app.modules.users.schemas.user import (
    UserResponse,
    UpdateProfileRequest,
    ChangePasswordRequest,
)
from app.modules.users.schemas.settings import (
    UserSettingResponse,
    UserSettingUpdate,
)
from app.modules.users.schemas.activity import UserActivityResponse
from app.modules.users.services.user import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.put("/me", response_model=dict)
def update_profile(
    payload: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = user_service.update_user_profile(
        db, user_id=current_user.id, full_name=payload.full_name
    )
    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": UserResponse.model_validate(updated_user)
    }

@router.put("/me/password", response_model=dict)
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_service.change_password(db, user_id=current_user.id, data=payload)
    return {
        "success": True,
        "message": "Password changed successfully. Please log in again.",
        "data": None
    }

@router.post("/me/avatar", response_model=dict)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = await user_service.upload_avatar(
        db, user_id=current_user.id, file=file
    )
    return {
        "success": True,
        "message": "Avatar uploaded successfully",
        "data": UserResponse.model_validate(updated_user)
    }

@router.get("/me/settings", response_model=dict)
def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settings = user_service.get_settings(db, user_id=current_user.id)
    return {
        "success": True,
        "message": "Preferences retrieved successfully",
        "data": UserSettingResponse.model_validate(settings)
    }

@router.put("/me/settings", response_model=dict)
def update_settings(
    payload: UserSettingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_settings = user_service.update_settings(
        db, user_id=current_user.id, settings_in=payload
    )
    return {
        "success": True,
        "message": "Preferences updated successfully",
        "data": UserSettingResponse.model_validate(updated_settings)
    }

@router.get("/me/activities", response_model=dict)
def get_activities(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activities = user_service.get_activities(
        db, user_id=current_user.id, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Activity logs retrieved successfully",
        "data": [UserActivityResponse.model_validate(act) for act in activities]
    }
