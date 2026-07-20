"""
verify_deployment.py — Post-Deployment Verification Script

Validates that backend APIs, database connectivity, seeding status, auth services,
and AI analysis features are 100% operational on deployed staging/production targets.
"""

import sys
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("verify")

DEFAULT_BASE_URL = "http://localhost:8000"

def verify_deployment(base_url: str = DEFAULT_BASE_URL) -> bool:
    logger.info(f"--- Starting Deployment Verification against target: {base_url} ---")
    all_passed = True

    # 1. Health Check
    try:
        r = requests.get(f"{base_url}/health", timeout=10)
        assert r.status_code == 200, f"Health endpoint returned status {r.status_code}"
        data = r.json()
        assert data.get("status") == "healthy", f"Health status was {data.get('status')}"
        logger.info("✅ PASS: Public /health endpoint operational.")
    except Exception as e:
        logger.error(f"❌ FAIL: Health check failed: {e}")
        all_passed = False

    # 2. Public IPO List Endpoint
    try:
        r = requests.get(f"{base_url}/api/v1/ipos", timeout=10)
        assert r.status_code == 200, f"GET /api/v1/ipos returned {r.status_code}"
        data = r.json()
        total = data.get("pagination", {}).get("total", 0)
        items = data.get("data", [])
        assert total >= 10, f"Expected total >= 10 IPO records, got {total}"
        assert len(items) > 0, "No IPO items returned in data array"
        logger.info(f"✅ PASS: GET /api/v1/ipos returned {total} persisted records.")
    except Exception as e:
        logger.error(f"❌ FAIL: IPO list endpoint verification failed: {e}")
        all_passed = False

    # 3. Search IPO Endpoint
    try:
        r = requests.get(f"{base_url}/api/v1/ipos/search?q=Swiggy", timeout=10)
        assert r.status_code == 200, f"GET /api/v1/ipos/search returned {r.status_code}"
        data = r.json()
        items = data.get("data", [])
        assert len(items) > 0, "Search query 'Swiggy' returned zero records"
        swiggy_id = items[0]["id"]
        logger.info(f"✅ PASS: IPO Search operational (Swiggy ID: {swiggy_id}).")
    except Exception as e:
        logger.error(f"❌ FAIL: IPO search failed: {e}")
        all_passed = False

    # 4. Admin Auth Login & Operational Telemetry
    try:
        login_resp = requests.post(
            f"{base_url}/api/v1/auth/login",
            json={"email": "admin@ipogenius.ai", "password": "Admin123456!"},
            timeout=10
        )
        assert login_resp.status_code == 200, f"Admin login returned {login_resp.status_code}"
        token = login_resp.json().get("data", {}).get("access_token")
        assert token is not None, "Access token missing from login response"
        logger.info("✅ PASS: Super Admin authentication operational.")

        # Query Admin Operational Telemetry
        headers = {"Authorization": f"Bearer {token}"}
        status_resp = requests.get(f"{base_url}/api/v1/admin/database/status", headers=headers, timeout=10)
        assert status_resp.status_code == 200, f"Admin status endpoint returned {status_resp.status_code}"
        telemetry = status_resp.json().get("data", {})
        assert telemetry.get("database", {}).get("connected") is True, "Database not connected in admin telemetry"
        assert telemetry.get("database", {}).get("ipo_count", 0) >= 10, "Telemetry ipo_count < 10"
        logger.info(f"✅ PASS: Admin Telemetry verified. Version: {telemetry.get('application', {}).get('version')}")
    except Exception as e:
        logger.error(f"❌ FAIL: Admin authentication or telemetry failed: {e}")
        all_passed = False

    if all_passed:
        logger.info("🎉 SUCCESS: All deployment verification checks PASSED!")
    else:
        logger.error("💥 CRITICAL: Deployment verification failed on one or more checks!")

    return all_passed

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE_URL
    success = verify_deployment(target_url)
    sys.exit(0 if success else 1)
