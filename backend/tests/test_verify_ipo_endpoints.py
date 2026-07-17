import pytest
import json
import uuid
import datetime
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail

def test_verify_ipo_endpoints_trace(client, mock_db):
    ipo_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    sample_ipo = IPO(
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
    sample_ipo.details = details

    print("\n==================================================")
    print("VERIFYING IPO MODULE ENDPOINTS")
    print("==================================================")

    # 1. Verify GET /ipos
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().order_by().offset().limit().all.return_value = [sample_ipo]
    print("\n--- 1. GET /api/v1/ipos ---")
    res = client.get("/api/v1/ipos?limit=5&offset=0")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 2. Verify GET /ipos/open
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().filter().order_by().offset().limit().all.return_value = [sample_ipo]
    print("\n--- 2. GET /api/v1/ipos/open ---")
    res = client.get("/api/v1/ipos/open")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 3. Verify GET /ipos/upcoming
    sample_ipo.status = IPOStatus.UPCOMING
    print("\n--- 3. GET /api/v1/ipos/upcoming ---")
    res = client.get("/api/v1/ipos/upcoming")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # Restore status to Open
    sample_ipo.status = IPOStatus.OPEN

    # 4. Verify GET /ipos/search
    mock_db.query().options().count.return_value = 1
    mock_db.query().options().filter().order_by().offset().limit().all.return_value = [sample_ipo]
    print("\n--- 4. GET /api/v1/ipos/search?q=Genius ---")
    res = client.get("/api/v1/ipos/search?q=Genius")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 5. Verify GET /ipos/{id}
    mock_db.query().options().filter().first.side_effect = None
    mock_db.query().options().filter().first.return_value = sample_ipo
    print("\n--- 5. GET /api/v1/ipos/{id} ---")
    res = client.get(f"/api/v1/ipos/{ipo_id}")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 6. Verify GET /ipos/{slug}
    mock_db.query().options().filter().first.return_value = sample_ipo
    print("\n--- 6. GET /api/v1/ipos/{slug} ---")
    res = client.get("/api/v1/ipos/genius-tech-ltd")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print("==================================================")
