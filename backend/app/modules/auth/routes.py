from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.auth.schemas import (
    APIResponse,
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenData,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.modules.users.schemas import UserCreate, UserResponse
from app.modules.users.models import User
from app.modules.auth.services import auth_service
from app.shared.dependencies import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger("app")

@router.post("/auth/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    logger.info(f"Register request for email: {request.email}")
    user_in = UserCreate(
        full_name=request.full_name,
        email=request.email,
        password=request.password
    )
    user = auth_service.register_user(db, user_in)
    
    # Wrap in UserResponse
    user_resp = UserResponse.model_validate(user)
    return APIResponse(
        success=True,
        message="Registration successful",
        data=user_resp
    )

@router.post("/auth/login", response_model=APIResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login request for email: {request.email}")
    user, access_token, refresh_token = auth_service.login_user(
        db, email=request.email, password=request.password
    )
    
    token_data = TokenData(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )
    return APIResponse(
        success=True,
        message="Login successful",
        data=token_data
    )

@router.post("/auth/refresh", response_model=APIResponse)
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    logger.info("Token refresh request received")
    user, access_token, refresh_token = auth_service.refresh_access_token(
        db, refresh_token=request.refresh_token
    )
    
    token_data = TokenData(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )
    return APIResponse(
        success=True,
        message="Token refreshed",
        data=token_data
    )

@router.post("/auth/logout", response_model=APIResponse)
def logout(request: RefreshTokenRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"Logout request from user {current_user.id}")
    auth_service.revoke_refresh_token(db, request.refresh_token)
    return APIResponse(
        success=True,
        message="Logout successful"
    )

@router.post("/auth/forgot-password", response_model=APIResponse)
def forgot_password(request: Request, body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    from app.shared.rate_limiter import forgot_password_limiter
    # Rate limit by client IP address
    ip_key = request.client.host if request.client else "unknown"
    forgot_password_limiter.check_rate_limit(ip_key)

    logger.info("Forgot password link requested")
    auth_service.request_password_reset(db, body.email)
    return APIResponse(
        success=True,
        message="If the email exists, a password reset link has been sent."
    )

@router.post("/auth/reset-password", response_model=APIResponse)
def reset_password(request: Request, body: ResetPasswordRequest, db: Session = Depends(get_db)):
    from app.shared.rate_limiter import reset_password_limiter
    # Rate limit by client IP address
    ip_key = request.client.host if request.client else "unknown"
    reset_password_limiter.check_rate_limit(ip_key)

    logger.info("Reset password request received")
    auth_service.reset_password(db, body.token, body.new_password)
    return APIResponse(
        success=True,
        message="Password has been reset successfully"
    )

@router.get("/users/me", response_model=APIResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    user_resp = UserResponse.model_validate(current_user)
    return APIResponse(
        success=True,
        message="Profile fetched",
        data=user_resp
    )

