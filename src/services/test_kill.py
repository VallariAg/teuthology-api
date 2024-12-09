from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app


client = TestClient(app)


@patch("app.main.teuthology.kill.main")
def test_kill_job_success(mock_teuthology_kill_main):
    mock_teuthology_kill_main.return_value = None
    response = client.post(
        "/kill",
        json={"run": "run1"},
        headers={"Authorization": "Bearer access_token"},
    )
    assert response.status_code == 200
    assert response.json() == {"kill": "success"}


def test_missing_access_token():
    response = client.post("/kill", json={"run": "run1"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You need to be logged in",
        "headers": {"WWW-Authenticate": "Bearer"},
        "status_code": 401,
    }


def test_missing_run_argument():
    response = client.post(
        "/kill",
        headers={"Authorization": "Bearer access_token"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "--run is a required argument", "status_code": 400}


@patch("app.main.get_username")
def test_insufficient_permission(mock_get_username):
    mock_get_username.return_value = "user1"
    response = client.post(
        "/kill",
        json={"run": "run1"},
        headers={"Authorization": "Bearer access_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You don't have permission to kill this run/job",
        "status_code": 401,
    }





















































