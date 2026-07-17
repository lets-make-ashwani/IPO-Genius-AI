from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from app.modules.subscriptions.models.payment import PaymentStatus

class PaymentCreateOrderRequest(BaseModel):
    plan_id: uuid.UUID

class PaymentCreateOrderResponse(BaseModel):
    provider_order_id: str
    amount: int
    currency: str
    status: str

class PaymentVerifyRequest(BaseModel):
    provider_order_id: str
    provider_payment_id: str
    provider_signature: str

class PaymentTransactionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan_id: uuid.UUID
    plan_code: str
    amount: int
    currency: str
    status: PaymentStatus
    provider: str
    provider_order_id: str
    provider_payment_id: str | None = None
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
