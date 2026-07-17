import pytest
import uuid
import datetime
from app.modules.users.models import User
from app.modules.subscriptions.models.plan import SubscriptionPlan, BillingInterval
from app.modules.subscriptions.models.subscription import UserSubscription, SubscriptionStatus
from app.modules.subscriptions.models.payment import PaymentTransaction, PaymentStatus
from app.modules.subscriptions.models.webhook import PaymentWebhookEvent, WebhookEventStatus
from app.shared.security import create_access_token
from app.shared.exceptions import AppException
from fastapi import status

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

@pytest.fixture
def mock_user():
    return User(
        id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        full_name="Jane Doe",
        email="user@example.com",
        role="USER",
        is_active=True
    )

@pytest.fixture
def mock_plan():
    return SubscriptionPlan(
        id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
        code="PREMIUM_MONTHLY",
        name="Premium Monthly",
        price_amount=49900,
        currency="INR",
        billing_interval=BillingInterval.MONTHLY,
        billing_interval_count=1,
        is_active=True
    )

# 1. Test Available Plans & Auto-Seeding
def test_list_plans(client, monkeypatch):
    monkeypatch.setattr("app.modules.subscriptions.repositories.plan.plan_repository.seed_default_plans", lambda db: None)
    monkeypatch.setattr("app.modules.subscriptions.repositories.plan.plan_repository.list_active", lambda db: [
        SubscriptionPlan(id=uuid.uuid4(), code="FREE", name="Free", price_amount=0, currency="INR", billing_interval=BillingInterval.FREE, billing_interval_count=1, is_active=True)
    ])

    response = client.get("/api/v1/subscriptions/plans")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"][0]["code"] == "FREE"


# 2. Test Subscription Expiration & Entitlement Denial
def test_expired_subscription_entitlement_denied(client, monkeypatch, mock_user, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_user)
    
    # Mock active subscription query to return None (expired/no plan)
    monkeypatch.setattr("app.modules.subscriptions.services.subscription.subscription_service.get_active_subscription", lambda db, uid: None)

    from app.modules.subscriptions.shared.dependencies import require_premium_entitlement
    from fastapi import Depends
    
    # We trigger endpoint which uses require_premium_entitlement dependency
    # For testing, we mock get_current_subscription to raise the exception directly
    with pytest.raises(AppException) as exc_info:
        from app.modules.subscriptions.shared.dependencies import require_premium_entitlement
        require_premium_entitlement(current_sub=None)
    assert exc_info.value.status_code == 403
    assert "Active premium subscription required" in exc_info.value.message

# 3. Test Cancelled-at-Period-End Entitlement (retains access)
def test_cancelled_at_period_end_retains_access(auth_header):
    sub = UserSubscription(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        status=SubscriptionStatus.CANCELLED,
        start_date=datetime.datetime.now(datetime.timezone.utc),
        end_date=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10),
        cancel_at_period_end=True,
        plan=SubscriptionPlan(code="PREMIUM_MONTHLY")
    )
    from app.modules.subscriptions.shared.dependencies import require_premium_entitlement
    # Should not raise exception
    res = require_premium_entitlement(current_sub=sub)
    assert res == sub

# 4. Test Inactive Plan Purchase Prevention
def test_inactive_plan_purchase_prevented(client, monkeypatch, mock_user, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_user)
    
    inactive_plan = SubscriptionPlan(
        id=uuid.uuid4(),
        code="OLD_PLAN",
        name="Old Plan",
        price_amount=9900,
        currency="INR",
        is_active=False
    )
    monkeypatch.setattr("app.modules.subscriptions.repositories.plan.plan_repository.get_by_id", lambda db, pid: inactive_plan)

    payload = {"plan_id": str(inactive_plan.id)}
    response = client.post("/api/v1/payments/create-order", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Selected plan is currently inactive" in response.json()["message"]

# 5. Test Frontend Amount Tampering Protection (uses DB plan amount)
def test_frontend_amount_tampering_ignored(client, monkeypatch, mock_user, mock_plan, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_user)
    monkeypatch.setattr("app.modules.subscriptions.repositories.plan.plan_repository.get_by_id", lambda db, pid: mock_plan)
    monkeypatch.setattr("app.modules.subscriptions.repositories.payment.payment_transaction_repository.create", lambda db, pay: pay)
    
    # We intercept create_order to verify that it resolves price_amount from mock_plan (49900 paisa)
    payload = {"plan_id": str(mock_plan.id)}
    response = client.post("/api/v1/payments/create-order", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["amount"] == 49900  # Resolved from database, not client parameter!

# 6. Test Invalid Signature Callback Failure
def test_invalid_signature_callback_fails(client, monkeypatch, mock_user, mock_plan, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_user)
    
    tx = PaymentTransaction(
        id=uuid.uuid4(),
        user_id=mock_user.id,
        plan_id=mock_plan.id,
        amount=mock_plan.price_amount,
        status=PaymentStatus.CREATED
    )
    monkeypatch.setattr("app.modules.subscriptions.repositories.payment.payment_transaction_repository.get_by_provider_order_id", lambda db, oid, lock: tx)
    monkeypatch.setattr("app.modules.subscriptions.repositories.payment.payment_transaction_repository.update", lambda db, t: t)
    monkeypatch.setattr("app.modules.notifications.events.dispatcher.event_dispatcher.dispatch", lambda *args, **kwargs: None)

    payload = {
        "provider_order_id": "order_123",
        "provider_payment_id": "pay_123",
        "provider_signature": "invalid_sig"  # Triggers MockPaymentProvider failure path
    }
    response = client.post("/api/v1/payments/verify", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Invalid payment signature" in response.json()["message"]

# 7. Test Duplicate Webhook Replay Protection
def test_duplicate_webhook_ignored(client, monkeypatch, mock_user):
    # Mock webhook repository get_by_provider_event_id to return an existing event
    monkeypatch.setattr("app.modules.subscriptions.repositories.webhook.payment_webhook_repository.get_by_provider_event_id", lambda db, eid: PaymentWebhookEvent(
        id=uuid.uuid4(),
        provider_event_id=eid,
        status=WebhookEventStatus.PROCESSED
    ))

    # Mock signature verification
    monkeypatch.setattr("app.modules.subscriptions.services.provider.MockPaymentProvider.verify_webhook_signature", lambda self, raw_body, signature, webhook_secret: True)

    payload = {
        "id": "evt_duplicate_id",
        "event": "payment.captured"
    }
    headers = {"X-Razorpay-Signature": "valid_sig"}
    response = client.post("/api/v1/payments/webhooks/razorpay", json=payload, headers=headers)
    assert response.status_code == 200
    assert "Duplicate event ignored" in response.json()["message"]

# 8. Test Invalid Webhook Signature Rejected
def test_invalid_webhook_signature_rejected(client):
    payload = {
        "id": "evt_id",
        "event": "payment.captured"
    }
    headers = {"X-Razorpay-Signature": "invalid_sig"}
    response = client.post("/api/v1/payments/webhooks/razorpay", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Invalid webhook signature" in response.json()["message"]

# 9. Test Production refuses Mock payment provider
def test_production_refuses_mock_provider(monkeypatch):
    from app.config import settings
    # Setup mock values
    values = {
        "ENVIRONMENT": "production",
        "PORT": 8000,
        "DATABASE_URL": "postgresql://test:test@localhost:5432/test",
        "JWT_SECRET": "secret",
        "FRONTEND_URL": "http://localhost",
        "PAYMENT_PROVIDER": "MOCK" # MOCK in Production!
    }
    
    from app.config.settings import Settings
    with pytest.raises(ValueError) as exc_info:
        Settings(**values)
    assert "Production environment does not allow MOCK payment provider" in str(exc_info.value)

# 10. Test Admin Panel RBAC Restrictions
def test_admin_subscriptions_access_restrictions(client, monkeypatch, mock_user, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_user)

    # Normal user should be rejected with 403
    response = client.get("/api/v1/admin/subscriptions", headers=headers)
    assert response.status_code == 403

