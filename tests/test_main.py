from src.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["root"] == "success"


def test_kill_no_auth():
    response = client.post("/kill")
    assert response.status_code == 401
    assert response.json() == {"detail": "You need to be logged in"}


def test_suite_no_auth():
    response = client.post("/suite")
    assert response.status_code == 401
    assert response.json() == {"detail": "You need to be logged in"}
