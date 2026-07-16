from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.users.models import User
from app.modules.users.repositories import user_repository
from app.shared.security import decode_token
from app.shared.exceptions import AppException
import uuid

reusable_oauth2 = HTTPBearer(auto_error=False)

def get_current_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)
) -> User:
    if not token:
        raise AppException("Not authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
        
    payload = decode_token(token.credentials)
    if not payload or payload.get("type") != "access":
        raise AppException("Could not validate credentials", status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_id = payload.get("sub")
    if not user_id:
        raise AppException("Could not validate credentials", status_code=status.HTTP_401_UNAUTHORIZED)
        
    try:
        uuid_user_id = uuid.UUID(user_id)
    except ValueError:
        raise AppException("Invalid credentials payload", status_code=status.HTTP_401_UNAUTHORIZED)
        
    user = user_repository.get_by_id(db, uuid_user_id)
    if not user or not user.is_active:
        raise AppException("User inactive or not found", status_code=status.HTTP_401_UNAUTHORIZED)
        
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise AppException("Forbidden: Not enough permissions", status_code=status.HTTP_403_FORBIDDEN)
        return current_user
