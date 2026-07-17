import pytest
import uuid
import datetime
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail

@pytest.fixture
def sample_ipo():
    ipo_id = uuid.uuid4()
    ipo = IPO(
        id=ipo_id,
        company_name="Genius Tech Ltd",
        slug="genius-tech-ltd",
        logo_url="https://example.com/logo.png",
        sector="Technology",
        industry="Software Services",
        exchange=IPOExchange.BOTH,
        ipo_type=IPOType.MAINBOARD,
        price_band="₹100 - ₹105",
        lot_size=140,
        issue_size="₹1,500 Cr",
        open_date=datetime.date(2026, 7, 20),
        close_date=datetime.date(2026, 7, 23),
        listing_date=datetime.date(2026, 7, 30),
        status=IPOStatus.OPEN,
        gmp=15,
        gmp_last_updated=datetime.datetime.now(datetime.timezone.utc),
        drhp_url="https://example.com/drhp",
        rhp_url="https://example.com/rhp",
        prospectus_url="https://example.com/prospectus",
        source="NSE",
        source_url="https://nseindia.com/genius",
        last_synced_at=datetime.datetime.now(datetime.timezone.utc),
        is_verified=True,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )
    
    details = IPODetail(
        id=uuid.uuid4(),
        ipo_id=ipo_id,
        company_overview="A leading tech service provider.",
        business_model="SaaS and consulting.",
        promoters="Mr. Genius",
        objectives="Debt repayment and general corporate purposes.",
        financial_summary="Revenue grew 20% YoY."
    )
    ipo.details = details
    return ipo

def test_get_all_ipos_success(client, mock_db, sample_ipo):
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().order_by().offset().limit().all.return_value = [sample_ipo]

    response = client.get("/api/v1/ipos")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["company_name"] == "Genius Tech Ltd"
    assert data["data"][0]["status"] == "Open"
    assert data["data"][0]["logo_url"] == "https://example.com/logo.png"
    assert data["meta"]["total"] == 1

def test_get_upcoming_ipos(client, mock_db, sample_ipo):
    sample_ipo.status = IPOStatus.UPCOMING
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().filter().order_by().offset().limit().all.return_value = [sample_ipo]

    response = client.get("/api/v1/ipos/upcoming")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"][0]["status"] == "Upcoming"

def test_get_open_ipos(client, mock_db, sample_ipo):
    sample_ipo.status = IPOStatus.OPEN
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().filter().order_by().offset().limit().all.return_value = [sample_ipo]

    response = client.get("/api/v1/ipos/open")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"][0]["status"] == "Open"

def test_get_closed_ipos(client, mock_db, sample_ipo):
    sample_ipo.status = IPOStatus.CLOSED
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().filter().order_by().offset().limit().all.return_value = [sample_ipo]

    response = client.get("/api/v1/ipos/closed")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"][0]["status"] == "Closed"

def test_get_listed_ipos(client, mock_db, sample_ipo):
    sample_ipo.status = IPOStatus.LISTED
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().filter().order_by().offset().limit().all.return_value = [sample_ipo]

    response = client.get("/api/v1/ipos/listed")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"][0]["status"] == "Listed"

def test_search_ipos(client, mock_db, sample_ipo):
    mock_db.query().options().count.return_value = 1
    # Mock filtering chain for search
    mock_db.query().options().filter().order_by().offset().limit().all.return_value = [sample_ipo]

    response = client.get("/api/v1/ipos/search?q=Genius")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"][0]["company_name"] == "Genius Tech Ltd"

def test_get_ipo_details_by_id(client, mock_db, sample_ipo):
    mock_db.query().options().filter().first.return_value = sample_ipo

    response = client.get(f"/api/v1/ipos/{sample_ipo.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["company_name"] == "Genius Tech Ltd"
    assert data["data"]["details"]["company_overview"] == "A leading tech service provider."

def test_get_ipo_details_by_slug(client, mock_db, sample_ipo):
    # To test slug matching, the UUID conversion will raise ValueError and trigger search by slug
    mock_db.query().options().filter().first.return_value = sample_ipo

    response = client.get("/api/v1/ipos/genius-tech-ltd")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["slug"] == "genius-tech-ltd"

def test_get_ipo_details_not_found(client, mock_db):
    mock_db.query().options().filter().first.return_value = None

    response = client.get(f"/api/v1/ipos/{uuid.uuid4()}")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "IPO not found" in data["message"]
