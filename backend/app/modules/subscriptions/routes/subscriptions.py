from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import datetime
import uuid

from app.database.session import get_db
from app.shared.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.subscriptions.schemas.plan import SubscriptionPlanResponse
from app.modules.subscriptions.schemas.subscription import UserSubscriptionResponse
from app.modules.subscriptions.repositories.plan import plan_repository
from app.modules.subscriptions.repositories.subscription import subscription_repository
from app.modules.subscriptions.models.subscription import UserSubscription, SubscriptionStatus
from app.modules.subscriptions.services.subscription import subscription_service
from app.shared.exceptions import AppException

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.get("/plans", response_model=Dict[str, Any])
def list_available_plans(db: Session = Depends(get_db)):
    # Seed default plans if not already populated (self-seeding safety)
    plan_repository.seed_default_plans(db)
    plans = plan_repository.list_active(db)
    return {
        "success": True,
        "message": "Plans retrieved successfully",
        "data": [SubscriptionPlanResponse.model_validate(p) for p in plans]
    }

@router.get("/me", response_model=Dict[str, Any])
def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan_repository.seed_default_plans(db)
    sub = subscription_service.get_active_subscription(db, current_user.id)
    
    if not sub:
        # Auto-provision FREE subscription plan
        free_plan = plan_repository.get_by_code(db, "FREE")
        if free_plan:
            now = datetime.datetime.now(datetime.timezone.utc)
            new_sub = UserSubscription(
                id=uuid.uuid4(),
                user_id=current_user.id,
                plan_id=free_plan.id,
                status=SubscriptionStatus.ACTIVE,
                start_date=now,
                end_date=now + datetime.timedelta(days=36500), # 100 years
                cancel_at_period_end=False,
                provider_subscription_id="free_provisioned",
                created_at=now,
                updated_at=now
            )
            sub = subscription_repository.create(db, new_sub)
        else:
            raise AppException("Free plan definition missing", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return {
        "success": True,
        "message": "Subscription retrieved successfully",
        "data": UserSubscriptionResponse.model_validate(sub)
    }

@router.post("/cancel", response_model=Dict[str, Any])
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sub = subscription_service.cancel_subscription(db, user_id=current_user.id)
    return {
        "success": True,
        "message": "Subscription cancelled successfully. You retain premium features until the billing cycle ends.",
        "data": UserSubscriptionResponse.model_validate(sub)
    }
