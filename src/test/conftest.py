import pytest
from fastapi.testclient import TestClient

from main import app
import uuid
import pathlib


def mock_get_token():
    return "access_token_imposter"


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    create test client instance
    """
    client = TestClient(app)
    yield client


@pytest.fixture
def archive_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(uuid, "uuid4", "tmp_log_file")
    archived_dir = tmp_path / "archive_dir"
    archived_dir.mkdir()
    (archived_dir / "tmp_log_file.log").touch()
    yield archived_dir


