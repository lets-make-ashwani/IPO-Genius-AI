from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.modules.subscriptions.models.webhook import PaymentWebhookEvent

class PaymentWebhookRepository:
    def get_by_id(self, db: Session, webhook_id: uuid.UUID) -> Optional[PaymentWebhookEvent]:
        return db.query(PaymentWebhookEvent).filter(PaymentWebhookEvent.id == webhook_id).first()

    def get_by_provider_event_id(self, db: Session, event_id: str) -> Optional[PaymentWebhookEvent]:
        return db.query(PaymentWebhookEvent).filter(PaymentWebhookEvent.provider_event_id == event_id).first()

    def create(self, db: Session, webhook_event: PaymentWebhookEvent) -> PaymentWebhookEvent:
        db.add(webhook_event)
        db.commit()
        db.refresh(webhook_event)
        return webhook_event

    def update(self, db: Session, webhook_event: PaymentWebhookEvent) -> PaymentWebhookEvent:
        db.commit()
        db.refresh(webhook_event)
        return webhook_event

payment_webhook_repository = PaymentWebhookRepository()
