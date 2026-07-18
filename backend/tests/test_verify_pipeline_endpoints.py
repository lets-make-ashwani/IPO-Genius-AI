import pytest
import uuid
import datetime
from app.modules.pipeline.models.pipeline import (
    PipelineRun,
    PipelineRunItem,
    PipelineRunStatus,
    PipelineRunTrigger,
    PipelineItemStatus,
    PipelineItemStage,
)
from app.modules.users.models.user import User

@pytest.fixture
def auth_admin_header():
    user_id = uuid.UUID("11111111-2222-3333-4444-555555555555")
    from app.shared.security import create_access_token
    token = create_access_token({"sub": str(user_id), "email": "admin@example.com", "role": "ADMIN"})
    return {"Authorization": f"Bearer {token}"}, user_id

@pytest.fixture
def auth_user_header():
    user_id = uuid.UUID("22222222-3333-4444-5555-666666666666")
    from app.shared.security import create_access_token
    token = create_access_token({"sub": str(user_id), "email": "user@example.com", "role": "USER"})
    return {"Authorization": f"Bearer {token}"}, user_id

@pytest.fixture
def mock_admin_user(auth_admin_header):
    _, uid = auth_admin_header
    return User(
        id=uid,
        full_name="Admin User",
        email="admin@example.com",
        password_hash="fake",
        role="ADMIN",
        is_active=True
    )

@pytest.fixture
def sample_pipeline_run():
    return PipelineRun(
        id=uuid.UUID("77777777-7777-7777-7777-777777777777"),
        idempotency_key="test_run_key",
        status=PipelineRunStatus.COMPLETED,
        trigger=PipelineRunTrigger.MANUAL,
        source_provider="MOCK",
        triggered_by_admin_id=uuid.UUID("11111111-2222-3333-4444-555555555555"),
        total_discovered=2,
        total_processed=2,
        total_skipped=0,
        total_failed=0,
        started_at=datetime.datetime.now(datetime.timezone.utc),
        completed_at=datetime.datetime.now(datetime.timezone.utc),
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

@pytest.fixture
def sample_pipeline_item():
    return PipelineRunItem(
        id=uuid.UUID("88888888-8888-8888-8888-888888888888"),
        run_id=uuid.UUID("77777777-7777-7777-7777-777777777777"),
        source_identifier="mock-item-1",
        company_name="Mock Item Company",
        status=PipelineItemStatus.COMPLETED,
        current_stage=PipelineItemStage.COMPLETED,
        retry_count=0,
        started_at=datetime.datetime.now(datetime.timezone.utc),
        completed_at=datetime.datetime.now(datetime.timezone.utc),
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

# 1. Test Authorization
def test_pipeline_run_endpoint_unauthorized(client):
    response = client.post("/api/v1/admin/pipeline/run", json={"provider": "MOCK"})
    assert response.status_code == 401

def test_pipeline_run_endpoint_forbidden_for_user(client, auth_user_header, monkeypatch):
    headers, uid = auth_user_header
    user = User(id=uid, full_name="User", email="u@ex.com", password_hash="f", role="USER", is_active=True)
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, u_id: user)
    
    response = client.post("/api/v1/admin/pipeline/run", json={"provider": "MOCK"}, headers=headers)
    assert response.status_code == 403

# 2. Trigger pipeline success
def test_trigger_pipeline_success(client, auth_admin_header, mock_admin_user, sample_pipeline_run, monkeypatch):
    headers, _ = auth_admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, u_id: mock_admin_user)
    monkeypatch.setattr(
        "app.modules.pipeline.services.pipeline.pipeline_service.execute_pipeline_run",
        lambda db, provider_name, trigger, admin_id, idempotency_key, force_reprocess: sample_pipeline_run
    )
    monkeypatch.setattr(
        "app.modules.users.repositories.activity.user_activity_repository.log_activity",
        lambda db, user_id, action, metadata_json: None
    )

    response = client.post("/api/v1/admin/pipeline/run", json={"provider": "MOCK"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["idempotency_key"] == "test_run_key"
    assert data["status"] == "COMPLETED"

# 3. Resume pipeline success
def test_resume_pipeline_success(client, auth_admin_header, mock_admin_user, sample_pipeline_run, monkeypatch):
    headers, _ = auth_admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, u_id: mock_admin_user)
    monkeypatch.setattr(
        "app.modules.pipeline.services.pipeline.pipeline_service.resume_pipeline_run",
        lambda db, run_id, force_reprocess: sample_pipeline_run
    )
    monkeypatch.setattr(
        "app.modules.users.repositories.activity.user_activity_repository.log_activity",
        lambda db, user_id, action, metadata_json: None
    )

    response = client.post(
        f"/api/v1/admin/pipeline/runs/{sample_pipeline_run.id}/resume",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"

# 4. GET pipeline runs list
def test_list_pipeline_runs(client, mock_db, auth_admin_header, mock_admin_user, sample_pipeline_run, monkeypatch):
    headers, _ = auth_admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, u_id: mock_admin_user)
    
    mock_db.query.return_value.count.return_value = 1
    mock_db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [sample_pipeline_run]
    mock_db.query.return_value.filter.return_value.count.return_value = 1
    mock_db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [sample_pipeline_run]

    response = client.get("/api/v1/admin/pipeline/runs", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["idempotency_key"] == "test_run_key"

# 5. GET pipeline run detail
def test_get_pipeline_run_detail(client, mock_db, auth_admin_header, mock_admin_user, sample_pipeline_run, sample_pipeline_item, monkeypatch):
    headers, _ = auth_admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, u_id: mock_admin_user)
    monkeypatch.setattr(
        "app.modules.pipeline.repositories.pipeline.pipeline_run_repository.get_by_id",
        lambda db, r_id: sample_pipeline_run
    )
    
    mock_db.query.return_value.filter.return_value.all.return_value = [sample_pipeline_item]

    response = client.get(f"/api/v1/admin/pipeline/runs/{sample_pipeline_run.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_pipeline_run.id)
    assert len(data["items"]) == 1
    assert data["items"][0]["source_identifier"] == "mock-item-1"

# 6. GET pipeline run item detail
def test_get_pipeline_run_item_detail(client, auth_admin_header, mock_admin_user, sample_pipeline_run, sample_pipeline_item, monkeypatch):
    headers, _ = auth_admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, u_id: mock_admin_user)
    monkeypatch.setattr(
        "app.modules.pipeline.repositories.pipeline.pipeline_run_item_repository.get_by_id",
        lambda db, i_id: sample_pipeline_item
    )

    response = client.get(
        f"/api/v1/admin/pipeline/runs/{sample_pipeline_run.id}/items/{sample_pipeline_item.id}",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_pipeline_item.id)
    assert data["company_name"] == "Mock Item Company"
