from sqlalchemy.orm import Session
import uuid
import datetime
import logging
from typing import Dict, Any

from app.modules.subscriptions.models.payment import PaymentTransaction, PaymentStatus
from app.modules.subscriptions.repositories.payment import payment_transaction_repository
from app.modules.subscriptions.repositories.plan import plan_repository
from app.modules.subscriptions.services.provider import get_payment_provider
from app.modules.subscriptions.services.subscription import subscription_service
from app.modules.users.repositories.activity import user_activity_repository
from app.shared.exceptions import AppException
from app.modules.notifications.events.dispatcher import event_dispatcher
from fastapi import status

logger = logging.getLogger("app")

class PaymentTransactionService:
    def create_order(self, db: Session, user_id: uuid.UUID, plan_id: uuid.UUID, idempotency_key: str = None) -> Dict[str, Any]:
        """
        Creates a payment order, snapshitting plan pricing, amount, and currency.
        """
        plan = plan_repository.get_by_id(db, plan_id)
        if not plan:
            raise AppException("Plan not found", status_code=status.HTTP_404_NOT_FOUND)
        if not plan.is_active:
            raise AppException("Selected plan is currently inactive", status_code=status.HTTP_400_BAD_REQUEST)

        # Idempotency check
        if idempotency_key:
            existing = db.query(PaymentTransaction).filter(
                PaymentTransaction.idempotency_key == idempotency_key
            ).first()
            if existing:
                logger.info(f"Duplicate order requested. Returning existing order {existing.provider_order_id}")
                return {
                    "provider_order_id": existing.provider_order_id,
                    "amount": existing.amount,
                    "currency": existing.currency,
                    "status": existing.status.value
                }

        # 1. Resolve payment details from Plan (NEVER trust frontend input!)
        amount_paisa = plan.price_amount
        currency = plan.currency

        # 2. Call Provider Layer
        provider = get_payment_provider()
        receipt_id = f"receipt_{uuid.uuid4().hex[:12]}"
        
        try:
            order = provider.create_order(amount_paisa=amount_paisa, currency=currency, receipt_id=receipt_id)
        except Exception as e:
            logger.error(f"Failed to create order with provider: {str(e)}")
            raise AppException("Payment provider error. Order creation failed.", status_code=status.HTTP_502_BAD_GATEWAY)

        # 3. Create transaction record
        payment = PaymentTransaction(
            id=uuid.uuid4(),
            user_id=user_id,
            plan_id=plan.id,
            plan_code=plan.code,
            amount=amount_paisa,
            currency=currency,
            status=PaymentStatus.CREATED,
            provider=settings_provider_name(),
            provider_order_id=order["id"],
            idempotency_key=idempotency_key,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )

        payment_transaction_repository.create(db, payment)

        return {
            "provider_order_id": payment.provider_order_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status.value
        }

    def verify_payment(
        self,
        db: Session,
        user_id: uuid.UUID,
        provider_order_id: str,
        provider_payment_id: str,
        provider_signature: str
    ) -> PaymentTransaction:
        """
        Verifies provider signature and transitions states securely.
        """
        # Row-level write lock
        payment = payment_transaction_repository.get_by_provider_order_id(db, provider_order_id, lock=True)
        if not payment:
            raise AppException("Payment transaction not found", status_code=status.HTTP_404_NOT_FOUND)

        if payment.status == PaymentStatus.SUCCESS:
            logger.info(f"Payment {provider_order_id} already marked SUCCESS. Returning early.")
            return payment

        # Ensure correct user owns the order
        if payment.user_id != user_id:
            raise AppException("Access denied: Order ownership mismatch", status_code=status.HTTP_403_FORBIDDEN)

        # State transition validation
        if payment.status not in [PaymentStatus.CREATED, PaymentStatus.PENDING]:
            raise AppException(f"Invalid payment state transition from {payment.status}", status_code=status.HTTP_400_BAD_REQUEST)

        # Verify signature
        provider = get_payment_provider()
        is_valid = provider.verify_payment_signature(
            order_id=provider_order_id,
            payment_id=provider_payment_id,
            signature=provider_signature
        )

        if not is_valid:
            payment.status = PaymentStatus.FAILED
            payment.error_message = "Signature verification failed"
            payment.updated_at = datetime.datetime.now(datetime.timezone.utc)
            payment_transaction_repository.update(db, payment)
            
            # Dispatch event
            event_dispatcher.dispatch(
                "PAYMENT_FAILED",
                db=db,
                user_id=user_id,
                payment_id=payment.id,
                error="Invalid signature"
            )
            
            raise AppException("Invalid payment signature verified", status_code=status.HTTP_400_BAD_REQUEST)

        # On success - activate subscription and update role if needed (Role remains USER/ADMIN)
        payment.status = PaymentStatus.SUCCESS
        payment.provider_payment_id = provider_payment_id
        # Discard signature parameter - do not save to DB permanently
        payment.provider_signature = None
        payment.updated_at = datetime.datetime.now(datetime.timezone.utc)

        # Activate subscription
        subscription_service.activate_subscription(db, user_id=user_id, payment=payment)
        payment_transaction_repository.update(db, payment)

        # Log Activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="PAYMENT_SUCCESS",
            metadata_json={"payment_id": str(payment.id), "amount": payment.amount}
        )

        # Dispatch decoupled event
        event_dispatcher.dispatch(
            "PAYMENT_SUCCESS",
            db=db,
            user_id=user_id,
            payment_id=payment.id,
            amount=payment.amount
        )

        return payment

def settings_provider_name() -> str:
    from app.config.settings import settings
    return settings.PAYMENT_PROVIDER.upper()

payment_transaction_service = PaymentTransactionService()
