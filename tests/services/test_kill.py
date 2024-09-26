import sys
sys.path.append('src')

import pytest
from fastapi.testclient import TestClient
import json
from src.main import app

client = TestClient(app)


def test_kill_job():
    response = client.post("/kill/job", json={"job_id": "1234"})
    assert response.status_code == 404
    if response.status_code == 200: 
        assert response.json() == {"success": True}

def test_kill_all(): 
    response = client.post("/kill/all")
    assert response.status_code == 404 
    if response.status_code == 200: 
        assert response.json() == {"success": True}


def test_kill_osd():
    response = client.post("/kill/osd", json={"osd_id": "123"})
    assert response.status_code == 404
    if response.status_code == 200:
        assert response.json() == {"success": True}

