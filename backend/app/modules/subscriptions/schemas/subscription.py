from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from app.modules.subscriptions.models.subscription import SubscriptionStatus
from app.modules.subscriptions.schemas.plan import SubscriptionPlanResponse

class UserSubscriptionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan_id: uuid.UUID
    status: SubscriptionStatus
    start_date: datetime.datetime
    end_date: datetime.datetime
    cancel_at_period_end: bool
    provider_subscription_id: str | None = None
    plan: SubscriptionPlanResponse | None = None

    model_config = ConfigDict(from_attributes=True)
