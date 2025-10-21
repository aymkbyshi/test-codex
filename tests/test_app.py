from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_pos_transactions():
    response = client.get("/pos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data, "Expected POS transactions to be returned"
    assert {"transaction_id", "store", "amount", "currency", "timestamp"}.issubset(data[0].keys())


def test_reservations():
    response = client.get("/reservations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data, "Expected reservation records to be returned"
    assert {"reservation_id", "restaurant", "party_size", "status", "reservation_time"}.issubset(
        data[0].keys()
    )


def test_analytics_summary():
    response = client.get("/analytics/revenue")
    assert response.status_code == 200
    payload = response.json()
    assert "revenue" in payload
    assert "occupancy" in payload
    assert payload["revenue"]["transaction_count"] > 0
