from fastapi import Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.shared.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.subscriptions.models.subscription import UserSubscription
from app.modules.subscriptions.services.subscription import subscription_service
from app.shared.exceptions import AppException

def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Optional[UserSubscription]:
    """
    Retrieves the currently active subscription of the logged-in user.
    """
    return subscription_service.get_active_subscription(db, current_user.id)

def require_premium_entitlement(
    current_sub: Optional[UserSubscription] = Depends(get_current_subscription)
) -> UserSubscription:
    """
    Dependency that enforces a valid, non-free active subscription.
    """
    if not current_sub:
        raise AppException("Active premium subscription required", status_code=status.HTTP_403_FORBIDDEN)
        
    if current_sub.plan and current_sub.plan.code == "FREE":
        raise AppException("Active premium subscription required", status_code=status.HTTP_403_FORBIDDEN)
        
    return current_sub
