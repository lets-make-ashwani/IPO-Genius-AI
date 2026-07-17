from pydantic import BaseModel, ConfigDict
import uuid
from app.modules.subscriptions.models.plan import BillingInterval

class SubscriptionPlanResponse(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    price_amount: int
    currency: str
    billing_interval: BillingInterval
    billing_interval_count: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
