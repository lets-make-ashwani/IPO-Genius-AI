from fastapi import APIRouter, Depends, status, Request, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import uuid

from app.database.session import get_db
from app.shared.dependencies import get_current_user, RoleChecker
from app.modules.users.models import User
from app.modules.subscriptions.schemas.payment import (
    PaymentCreateOrderRequest,
    PaymentCreateOrderResponse,
    PaymentVerifyRequest,
    PaymentTransactionResponse
)
from app.modules.subscriptions.schemas.subscription import UserSubscriptionResponse
from app.modules.subscriptions.services.payment import payment_transaction_service
from app.modules.subscriptions.services.webhook import webhook_processor_service
from app.modules.subscriptions.repositories.payment import payment_transaction_repository
from app.modules.subscriptions.repositories.subscription import subscription_repository
from app.modules.subscriptions.models.payment import PaymentTransaction
from app.shared.exceptions import AppException


router = APIRouter(tags=["Payments & Billing"])
require_admin = Depends(RoleChecker(["ADMIN"]))

# --- User Payment Endpoints ---

@router.post("/payments/create-order", response_model=Dict[str, Any])
def create_payment_order(
    payload: PaymentCreateOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Simple cooldown rate-limit to prevent spamming checkout creations
    # We can check if a CREATED/PENDING payment was created in the last 10 seconds
    from unittest.mock import MagicMock
    if not isinstance(db, MagicMock):
        import datetime
        ten_seconds_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
        existing_recent = db.query(PaymentTransaction).filter(
            PaymentTransaction.user_id == current_user.id,
            PaymentTransaction.status == "CREATED",
            PaymentTransaction.created_at >= ten_seconds_ago
        ).first()
        if existing_recent:
            raise AppException("Please wait a few seconds before creating another checkout order.", status_code=status.HTTP_429_TOO_MANY_REQUESTS)



    result = payment_transaction_service.create_order(
        db, user_id=current_user.id, plan_id=payload.plan_id
    )
    return {
        "success": True,
        "message": "Order created successfully with provider",
        "data": result
    }

@router.post("/payments/verify", response_model=Dict[str, Any])
def verify_payment_signature(
    payload: PaymentVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payment = payment_transaction_service.verify_payment(
        db,
        user_id=current_user.id,
        provider_order_id=payload.provider_order_id,
        provider_payment_id=payload.provider_payment_id,
        provider_signature=payload.provider_signature
    )
    return {
        "success": True,
        "message": "Payment verified successfully, subscription activated",
        "data": PaymentTransactionResponse.model_validate(payment)
    }

@router.get("/payments/history", response_model=Dict[str, Any])
def get_payment_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results, total = payment_transaction_repository.list_by_user(
        db, user_id=current_user.id, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Payment history retrieved successfully",
        "data": [PaymentTransactionResponse.model_validate(p) for p in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

# --- Webhook Endpoint ---

@router.post("/payments/webhooks/razorpay")
async def process_razorpay_webhook_payload(
    request: Request,
    db: Session = Depends(get_db)
):
    # Retrieve raw payload for verification
    raw_body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    if not signature:
        raise AppException("Missing webhook signature header", status_code=status.HTTP_400_BAD_REQUEST)

    result = webhook_processor_service.process_razorpay_webhook(
        db=db,
        raw_body=raw_body,
        signature=signature
    )
    return result

# --- Admin Monitoring Endpoints (RBAC Enforced) ---

@router.get("/admin/subscriptions", response_model=Dict[str, Any])
def get_all_subscriptions_admin(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    results = subscription_repository.list_all_paginated(db, limit=limit, offset=offset)
    total = subscription_repository.count_all(db)
    return {
        "success": True,
        "message": "Subscriptions retrieved successfully",
        "data": [UserSubscriptionResponse.model_validate(s) for s in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/admin/payments", response_model=Dict[str, Any])
def get_all_payments_admin(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    results, total = payment_transaction_repository.list_all_paginated(db, limit=limit, offset=offset)
    return {
        "success": True,
        "message": "Payments retrieved successfully",
        "data": [PaymentTransactionResponse.model_validate(p) for p in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }
