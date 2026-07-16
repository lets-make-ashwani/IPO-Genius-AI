from pydantic import BaseModel, EmailStr, Field
from typing import Any, Optional
from app.modules.users.schemas import UserResponse

class APIResponse(BaseModel):
    success: bool = True
    message: str = "Request successful"
    data: Optional[Any] = None

class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(...)

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(...)

class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6, max_length=100)
