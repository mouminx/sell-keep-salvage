import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)

def test_root_route():
    #sanity check for API
    response = client.get("/")
    assert response.status_code == 200
    assert "Sell/Keep/Salvage API" in response.json()["status"]

@patch("backend.main.evaluate_item")
def test_evaluate_mocked(mock_evaluate_item):
    #mock evaluator logic to verify and evaluate the endpoint
    #simulate evaluator returning a mock decision
    mock_evaluate_item.return_value = {
        "decision": "KEEP",
        "score": 0.87,
        "reasons": ["High strength", "good crit damage roll"],
    }

    #example request body (what client should send)
    payload = {
        "item_data": {
            "name": "Sacred Longsword",
            "affixes": ["+12 Strength", "+8% Critical Damage"],
        },
        "build_profile": {
            "class": "Barbarian",
            "preferred_affixes": ["strength", "crit damage"],
        },
    }

    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    result = data["result"]

    assert result["decision"] == "KEEP"
    assert result["score"] == pytest.approx(0.87, rel=1e-2)
    assert "reasons" in result and isinstance(result["reasons"], list)