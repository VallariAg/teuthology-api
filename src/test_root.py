import pytest

from conftest import mock_session_cookie, mock_session_data, test_client


def test_root():
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"root": "success", "session": mock_session_data["user"]}


def test_root_logged_out():
    test_client.cookies = {}
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"root": "success", "session": None}
