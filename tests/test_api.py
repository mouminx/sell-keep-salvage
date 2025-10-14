import io
import os
import pytest 
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_route():
    #verify the root (/) endpoint responds correctly
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "Sell/Keep/Salvage API" in data["status"]

@pytest.mark.skipif(not os.path.exists("data/samples/tooltip.png"), reason="Sample image missing")
def test_testocr_route():
    """Test the /test-ocr endpoint with a sample image upload."""
    sample_path = "data/samples/tooltip.png"
    with open(sample_path, "rb") as f:
        files = {"file": ("tooltip.png", f, "image/png")}
        response = client.post("/test-ocr", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "lines" in data
    assert isinstance(data["lines"], list)