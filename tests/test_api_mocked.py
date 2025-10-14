import numpy as np
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sell/Keep/Salvage API" in response.json()["status"]


@patch("backend.utils.preprocessing.cv2.cvtColor", return_value=np.zeros((100, 100, 3), dtype=np.uint8))
@patch("backend.main.extract_text")
def test_testocr_mocked(mock_extract_text, mock_cvtcolor):
    mock_extract_text.return_value = [
        "Sacred Longsword",
        "+12 Strength",
        "+8% Critical Damage",
        "+3% Resistance to All Elements",
    ]
    print("\n[DEBUG] Mock extract_text called with:", mock_extract_text.return_value)

    files = {"file": ("fake_image.png", b"fake_image_data", "image/png")}
    response = client.post("/test-ocr", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "lines" in data
    assert isinstance(data["lines"], list)
    assert len(data["lines"]) > 0
