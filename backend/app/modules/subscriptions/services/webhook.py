from sqlalchemy.orm import Session
import json
import datetime
import logging
import uuid
from typing import Dict, Any


from app.modules.subscriptions.models.webhook import PaymentWebhookEvent, WebhookEventStatus
from app.modules.subscriptions.models.payment import PaymentStatus
from app.modules.subscriptions.repositories.webhook import payment_webhook_repository
from app.modules.subscriptions.repositories.payment import payment_transaction_repository
from app.modules.subscriptions.services.provider import get_payment_provider
from app.modules.subscriptions.services.subscription import subscription_service
from app.modules.users.repositories.activity import user_activity_repository
from app.modules.notifications.events.dispatcher import event_dispatcher
from app.shared.exceptions import AppException
from fastapi import status

logger = logging.getLogger("app")

class WebhookProcessorService:
    def process_razorpay_webhook(self, db: Session, raw_body: bytes, signature: str) -> Dict[str, Any]:
        """
        Verifies signature, registers webhook events, and processes activations idempotently.
        """
        from app.config.settings import settings
        provider = get_payment_provider()

        # 1. Verify Signature
        # Note: Webhook secret must be set to run verification
        is_valid = provider.verify_webhook_signature(
            raw_body=raw_body,
            signature=signature,
            webhook_secret=settings.RAZORPAY_WEBHOOK_SECRET
        )

        if not is_valid:
            logger.warning("Invalid webhook signature received!")
            raise AppException("Invalid webhook signature", status_code=status.HTTP_400_BAD_REQUEST)

        # 2. Parse payload safely
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception:
            raise AppException("Invalid JSON payload", status_code=status.HTTP_400_BAD_REQUEST)

        # Razorpay webhook envelopes specify unique event ID in 'id' or a generated fallback
        provider_event_id = payload.get("id")
        if not provider_event_id:
            # Fallback to unique hash of body if provider ID is missing
            import hashlib
            provider_event_id = hashlib.sha256(raw_body).hexdigest()

        event_type = payload.get("event", "unknown")

        # 3. Deduplication check (idempotency / replay protection)
        existing = payment_webhook_repository.get_by_provider_event_id(db, provider_event_id)
        if existing:
            logger.info(f"Duplicate webhook event {provider_event_id} ignored.")
            return {"success": True, "message": "Duplicate event ignored", "status": existing.status.value}

        # 4. Save initial webhook log
        webhook_event = PaymentWebhookEvent(
            id=uuid_ref_generator(),
            provider="RAZORPAY",
            provider_event_id=provider_event_id,
            event_type=event_type,
            status=WebhookEventStatus.PENDING,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        payment_webhook_repository.create(db, webhook_event)

        # 5. Extract sanitized variables safely (no credit card or raw sensitive payload storage)
        entity_payload = payload.get("payload", {})
        payment_entity = entity_payload.get("payment", {}).get("entity", {})
        
        provider_order_id = payment_entity.get("order_id")
        provider_payment_id = payment_entity.get("id")
        payment_amount = payment_entity.get("amount")

        # Store a structured sanitized dictionary (no raw signatures, tokens, passwords)
        webhook_event.payload = {
            "order_id": provider_order_id,
            "payment_id": provider_payment_id,
            "amount": payment_amount,
            "event_type": event_type
        }

        # 6. Evaluate event type
        if event_type in ["payment.captured", "order.paid"] and provider_order_id:
            # Row-level write lock on payment transaction
            payment = payment_transaction_repository.get_by_provider_order_id(db, provider_order_id, lock=True)
            if payment:
                if payment.status == PaymentStatus.SUCCESS:
                    webhook_event.status = WebhookEventStatus.PROCESSED
                    webhook_event.processed_at = datetime.datetime.now(datetime.timezone.utc)
                    payment_webhook_repository.update(db, webhook_event)
                    return {"success": True, "message": "Payment already marked success", "status": "PROCESSED"}

                # Update payment status
                payment.status = PaymentStatus.SUCCESS
                payment.provider_payment_id = provider_payment_id
                payment.provider_signature = None # Discard sig
                payment.updated_at = datetime.datetime.now(datetime.timezone.utc)
                
                # Activate subscription
                subscription_service.activate_subscription(db, user_id=payment.user_id, payment=payment)
                payment_transaction_repository.update(db, payment)

                # Log Activity
                user_activity_repository.log_activity(
                    db,
                    user_id=payment.user_id,
                    action="PAYMENT_SUCCESS",
                    metadata_json={"payment_id": str(payment.id), "source": "webhook"}
                )

                # Dispatch event
                event_dispatcher.dispatch(
                    "PAYMENT_SUCCESS",
                    db=db,
                    user_id=payment.user_id,
                    payment_id=payment.id,
                    amount=payment.amount
                )

                webhook_event.status = WebhookEventStatus.PROCESSED
                webhook_event.processed_at = datetime.datetime.now(datetime.timezone.utc)
            else:
                webhook_event.status = WebhookEventStatus.FAILED
                webhook_event.error_message = f"Payment order {provider_order_id} not found"
        elif event_type == "payment.failed" and provider_order_id:
            payment = payment_transaction_repository.get_by_provider_order_id(db, provider_order_id, lock=True)
            if payment:
                payment.status = PaymentStatus.FAILED
                payment.error_message = payment_entity.get("error_description", "Payment failed")
                payment.updated_at = datetime.datetime.now(datetime.timezone.utc)
                payment_transaction_repository.update(db, payment)

                # Dispatch event
                event_dispatcher.dispatch(
                    "PAYMENT_FAILED",
                    db=db,
                    user_id=payment.user_id,
                    payment_id=payment.id,
                    error=payment.error_message
                )

                webhook_event.status = WebhookEventStatus.PROCESSED
                webhook_event.processed_at = datetime.datetime.now(datetime.timezone.utc)
            else:
                webhook_event.status = WebhookEventStatus.FAILED
                webhook_event.error_message = f"Payment order {provider_order_id} not found"
        else:
            # Ignore other events
            webhook_event.status = WebhookEventStatus.IGNORED

        payment_webhook_repository.update(db, webhook_event)
        return {"success": True, "message": "Webhook processed successfully", "status": webhook_event.status.value}

def uuid_ref_generator() -> uuid.UUID:
    import uuid
    return uuid.uuid4()

webhook_processor_service = WebhookProcessorService()
