import hmac
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger("app")

class BasePaymentProvider(ABC):
    @abstractmethod
    def create_order(self, amount_paisa: int, currency: str, receipt_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def verify_payment_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        pass

    @abstractmethod
    def verify_webhook_signature(self, raw_body: bytes, signature: str, webhook_secret: str) -> bool:
        pass


class MockPaymentProvider(BasePaymentProvider):
    def create_order(self, amount_paisa: int, currency: str, receipt_id: str) -> Dict[str, Any]:
        import uuid
        order_id = f"order_mock_{uuid.uuid4().hex[:12]}"
        logger.info(f"[MockPaymentProvider] Created mock order: {order_id} for amount {amount_paisa} {currency}")
        return {
            "id": order_id,
            "amount": amount_paisa,
            "currency": currency,
            "receipt": receipt_id,
            "status": "created"
        }

    def verify_payment_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        if signature == "invalid_sig":
            logger.warning("[MockPaymentProvider] Signature verification failed (explicit invalid_sig)")
            return False
        return True

    def verify_webhook_signature(self, raw_body: bytes, signature: str, webhook_secret: str) -> bool:
        if signature == "invalid_sig":
            logger.warning("[MockPaymentProvider] Webhook signature verification failed (explicit invalid_sig)")
            return False
        return True


class RazorpayProvider(BasePaymentProvider):
    def create_order(self, amount_paisa: int, currency: str, receipt_id: str) -> Dict[str, Any]:
        # Lazily import razorpay to avoid issues if SDK not installed
        try:
            import razorpay
            from app.config.settings import settings
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            data = {
                "amount": amount_paisa,
                "currency": currency,
                "receipt": receipt_id,
                "payment_capture": 1
            }
            order = client.order.create(data=data)
            return order
        except ImportError:
            logger.error("razorpay Python SDK not installed")
            raise Exception("Razorpay SDK not installed")
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {str(e)}")
            raise e

    def verify_payment_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        try:
            from app.config.settings import settings
            secret = settings.RAZORPAY_KEY_SECRET
            if not secret:
                return False
            
            # Compute signature using HMAC SHA256
            msg = f"{order_id}|{payment_id}".encode("utf-8")
            key = secret.encode("utf-8")
            generated = hmac.new(key, msg, hashlib.sha256).hexdigest()
            return hmac.compare_digest(generated, signature)
        except Exception as e:
            logger.error(f"Error verifying Razorpay payment signature: {str(e)}")
            return False

    def verify_webhook_signature(self, raw_body: bytes, signature: str, webhook_secret: str) -> bool:
        try:
            if not webhook_secret:
                return False
            key = webhook_secret.encode("utf-8")
            generated = hmac.new(key, raw_body, hashlib.sha256).hexdigest()
            return hmac.compare_digest(generated, signature)
        except Exception as e:
            logger.error(f"Error verifying Razorpay webhook signature: {str(e)}")
            return False

def get_payment_provider() -> BasePaymentProvider:
    from app.config.settings import settings
    prov_name = settings.PAYMENT_PROVIDER.upper()
    if prov_name == "RAZORPAY":
        return RazorpayProvider()
    return MockPaymentProvider()

