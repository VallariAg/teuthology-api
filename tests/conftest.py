import json
from base64 import b64encode
from itsdangerous import TimestampSigner

import pytest
from fastapi.testclient import TestClient

from src.main import app, SESSION_SECRET_KEY


@pytest.fixture()
def test_client():
    client = TestClient(app)
    yield client


mock_user_session = {
    "user": {
        "id": "mock_id",
        "username": "mock_username",
        "state": "mock_state",
        "role": "mock_role",
        "access_token": "mock_access_token",
    }
}


@pytest.fixture()
def test_client_auth():
    client = TestClient(app)
    # To store user session in the TestClient, the method that is
    # used by Starlette's SessionMiddleware for storing sessions
    # is implemented
    signer = TimestampSigner(SESSION_SECRET_KEY)
    data = b64encode(json.dumps(mock_user_session).encode("utf-8"))
    mock_session_cookies = signer.sign(data).decode("utf-8")
    client.cookies = {"session": mock_session_cookies}
    yield client
