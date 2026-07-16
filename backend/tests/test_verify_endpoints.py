import pytest
import json
import uuid
from datetime import datetime, timezone
from PIL import Image
import io
from app.modules.users.models.user import User
from app.modules.users.models.settings import UserSetting
from app.modules.users.models.activity import UserActivity, UserActivityType
from app.shared.security import get_password_hash, create_access_token

def generate_image_bytes():
    img = Image.new("RGB", (100, 100), color="blue")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()

def test_verify_user_endpoints_trace(client, mock_db):
    test_user_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    test_user = User(
        id=test_user_id,
        full_name="Jane Doe",
        email="jane@example.com",
        password_hash=get_password_hash("securepassword123"),
        avatar_url=None,
        role="USER",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    test_settings = UserSetting(
        id=uuid.uuid4(),
        user_id=test_user_id,
        theme="light",
        language="en",
        timezone="UTC",
        currency="USD",
        email_notifications=True,
        push_notifications=True,
        marketing_emails=False,
        date_format="YYYY-MM-DD",
        time_format="24h",
        first_day_of_week=1
    )

    test_activity = UserActivity(
        id=uuid.uuid4(),
        user_id=test_user_id,
        action=UserActivityType.LOGIN.value,
        metadata_json={"ip": "127.0.0.1"},
        created_at=datetime.now(timezone.utc)
    )

    # Generate JWT access token
    access_token = create_access_token({"sub": str(test_user_id), "email": test_user.email, "role": test_user.role})
    headers = {"Authorization": f"Bearer {access_token}"}

    print("\n==================================================")
    print("VERIFYING USER MODULE ENDPOINTS")
    print("==================================================")

    # 1. Verify PUT /users/me (Update Profile)
    mock_db.query().filter().first.return_value = test_user
    payload = {"full_name": "Jane Cooper"}
    print("\n--- 1. PUT /api/v1/users/me ---")
    print("Request Payload:", json.dumps(payload, indent=2))
    res = client.put("/api/v1/users/me", json=payload, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 2. Verify GET /users/me/settings
    mock_db.query().filter().first.side_effect = [test_user, test_settings]
    print("\n--- 2. GET /api/v1/users/me/settings ---")
    res = client.get("/api/v1/users/me/settings", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 3. Verify PUT /users/me/settings
    mock_db.query().filter().first.side_effect = [test_user, test_settings]
    payload_settings = {"theme": "dark", "timezone": "Asia/Kolkata", "push_notifications": False}
    print("\n--- 3. PUT /api/v1/users/me/settings ---")
    print("Request Payload:", json.dumps(payload_settings, indent=2))
    res = client.put("/api/v1/users/me/settings", json=payload_settings, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 4. Verify POST /users/me/avatar (with real PNG bytes)
    mock_db.query().filter().first.side_effect = None
    mock_db.query().filter().first.return_value = test_user
    print("\n--- 4. POST /api/v1/users/me/avatar ---")
    image_bytes = generate_image_bytes()
    res = client.post(
        "/api/v1/users/me/avatar",
        files={"file": ("avatar.png", image_bytes, "image/png")},
        headers=headers
    )
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 5. Verify GET /users/me/activities
    mock_db.query().filter().first.side_effect = None
    mock_db.query().filter().first.return_value = test_user
    mock_db.query().filter().order_by().offset().limit().all.return_value = [test_activity]
    print("\n--- 5. GET /api/v1/users/me/activities ---")
    res = client.get("/api/v1/users/me/activities?limit=10&offset=0", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 6. Verify PUT /users/me/password
    mock_db.query().filter().first.side_effect = None
    mock_db.query().filter().first.return_value = test_user

    payload_pw = {"old_password": "securepassword123", "new_password": "newsecurepassword123"}
    print("\n--- 6. PUT /api/v1/users/me/password ---")
    print("Request Payload:", json.dumps(payload_pw, indent=2))
    res = client.put("/api/v1/users/me/password", json=payload_pw, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print("==================================================")
