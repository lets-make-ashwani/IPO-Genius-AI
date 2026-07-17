from app.modules.subscriptions.routes.subscriptions import router as subscription_router
from app.modules.subscriptions.routes.payments import router as payment_router

__all__ = ["subscription_router", "payment_router"]
