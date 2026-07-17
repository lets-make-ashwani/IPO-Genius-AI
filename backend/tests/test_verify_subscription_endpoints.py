import pytest
import json
import uuid
import datetime
from app.modules.users.models import User
from app.modules.subscriptions.models.plan import SubscriptionPlan, BillingInterval
from app.modules.subscriptions.models.subscription import UserSubscription, SubscriptionStatus
from app.modules.subscriptions.models.payment import PaymentTransaction, PaymentStatus
from app.modules.subscriptions.models.webhook import PaymentWebhookEvent, WebhookEventStatus
from app.shared.security import create_access_token

@pytest.fixture
def auth_header():
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    token = create_access_token({"sub": str(user_id), "email": "user@example.com", "role": "USER"})
    return {"Authorization": f"Bearer {token}"}, user_id

@pytest.fixture
def admin_header():
    admin_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    token = create_access_token({"sub": str(admin_id), "email": "admin@example.com", "role": "ADMIN"})
    return {"Authorization": f"Bearer {token}"}, admin_id

def test_verify_subscription_endpoints_trace(client, monkeypatch, auth_header, admin_header):
    user_headers, user_id = auth_header
    admin_headers, admin_id = admin_header

    user = User(
        id=user_id,
        full_name="Jane Doe",
        email="user@example.com",
        role="USER",
        is_active=True
    )

    admin_user = User(
        id=admin_id,
        full_name="Admin User",
        email="admin@example.com",
        role="ADMIN",
        is_active=True
    )

    plan = SubscriptionPlan(
        id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
        code="PREMIUM_MONTHLY",
        name="Premium Monthly Plan",
        price_amount=49900,
        currency="INR",
        billing_interval=BillingInterval.MONTHLY,
        billing_interval_count=1,
        is_active=True,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

    sub = UserSubscription(
        id=uuid.UUID("44444444-4444-4444-4444-444444444444"),
        user_id=user_id,
        plan_id=plan.id,
        status=SubscriptionStatus.ACTIVE,
        start_date=datetime.datetime.now(datetime.timezone.utc),
        end_date=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30),
        cancel_at_period_end=False,
        provider_subscription_id="order_order_id_123",
        plan=plan,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

    tx = PaymentTransaction(
        id=uuid.UUID("77777777-7777-7777-7777-777777777777"),
        user_id=user_id,
        subscription_id=sub.id,
        plan_id=plan.id,
        plan_code=plan.code,
        amount=plan.price_amount,
        currency=plan.currency,
        status=PaymentStatus.SUCCESS,
        provider="MOCK",
        provider_order_id="order_order_id_123",
        provider_payment_id="pay_payment_id_123",
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

    # Monkeypatching Database operations & Services
    def mock_get_user(db, uid):
        if uid == user_id:
            return user
        if uid == admin_id:
            return admin_user
        return None

    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", mock_get_user)
    monkeypatch.setattr("app.modules.subscriptions.repositories.plan.plan_repository.list_active", lambda db: [plan])
    monkeypatch.setattr("app.modules.subscriptions.repositories.plan.plan_repository.get_by_id", lambda db, pid: plan)
    monkeypatch.setattr("app.modules.subscriptions.repositories.plan.plan_repository.seed_default_plans", lambda db: None)
    monkeypatch.setattr("app.modules.subscriptions.services.subscription.subscription_service.get_active_subscription", lambda db, uid: sub)
    monkeypatch.setattr("app.modules.subscriptions.services.subscription.subscription_service.cancel_subscription", lambda db, user_id: sub)
    monkeypatch.setattr("app.modules.subscriptions.repositories.payment.payment_transaction_repository.list_by_user", lambda db, user_id, limit, offset: ([tx], 1))
    monkeypatch.setattr("app.modules.subscriptions.repositories.payment.payment_transaction_repository.list_all_paginated", lambda db, limit, offset: ([tx], 1))
    monkeypatch.setattr("app.modules.subscriptions.repositories.subscription.subscription_repository.list_all_paginated", lambda db, limit, offset: [sub])
    monkeypatch.setattr("app.modules.subscriptions.repositories.subscription.subscription_repository.count_all", lambda db: 1)
    
    # Mocking order creations
    monkeypatch.setattr("app.modules.subscriptions.services.payment.payment_transaction_service.create_order", lambda db, user_id, plan_id: {
        "provider_order_id": "order_order_id_123",
        "amount": plan.price_amount,
        "currency": plan.currency,
        "status": "CREATED"
    })
    
    # Mocking payment verification
    monkeypatch.setattr("app.modules.subscriptions.services.payment.payment_transaction_service.verify_payment", lambda db, user_id, provider_order_id, provider_payment_id, provider_signature: tx)
    
    # Mocking webhook processing
    monkeypatch.setattr("app.modules.subscriptions.services.webhook.webhook_processor_service.process_razorpay_webhook", lambda db, raw_body, signature: {
        "success": True,
        "message": "Webhook processed successfully",
        "status": "PROCESSED"
    })

    print("\n==================================================")
    print("VERIFYING PAYMENT & SUBSCRIPTIONS MODULE ENDPOINTS")
    print("==================================================")

    # 1. GET /subscriptions/plans
    print("\n--- 1. GET /api/v1/subscriptions/plans ---")
    res = client.get("/api/v1/subscriptions/plans")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 2. GET /subscriptions/me
    print("\n--- 2. GET /api/v1/subscriptions/me ---")
    res = client.get("/api/v1/subscriptions/me", headers=user_headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 3. POST /payments/create-order
    print("\n--- 3. POST /api/v1/payments/create-order ---")
    res = client.post("/api/v1/payments/create-order", json={"plan_id": str(plan.id)}, headers=user_headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 4. POST /payments/verify
    print("\n--- 4. POST /api/v1/payments/verify ---")
    payload_verify = {
        "provider_order_id": "order_order_id_123",
        "provider_payment_id": "pay_payment_id_123",
        "provider_signature": "signature_123"
    }
    res = client.post("/api/v1/payments/verify", json=payload_verify, headers=user_headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 5. GET /payments/history
    print("\n--- 5. GET /api/v1/payments/history ---")
    res = client.get("/api/v1/payments/history", headers=user_headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 6. POST /subscriptions/cancel
    print("\n--- 6. POST /api/v1/subscriptions/cancel ---")
    res = client.post("/api/v1/subscriptions/cancel", headers=user_headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 7. GET /admin/subscriptions
    print("\n--- 7. GET /api/v1/admin/subscriptions ---")
    res = client.get("/api/v1/admin/subscriptions", headers=admin_headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 8. GET /admin/payments
    print("\n--- 8. GET /api/v1/admin/payments ---")
    res = client.get("/api/v1/admin/payments", headers=admin_headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print("==================================================")
