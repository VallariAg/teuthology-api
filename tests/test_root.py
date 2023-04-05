from .conftest import mock_user_session


def test_root_no_auth(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"root": "success", "session": None}


def test_root(test_client_auth):
    response = test_client_auth.get("/")
    assert response.status_code == 200
    assert response.json() == {"root": "success", "session": mock_user_session["user"]}
