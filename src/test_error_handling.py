from fastapi.testclient import TestClient
from app import app
import pytest


client = TestClient(app)

def test_invalid_job_id():
    response = client.get("/jobs/1234")
    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}

def test_missing_parameter():
    response = client.post("/jobs/run", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "config"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
