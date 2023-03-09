from fastapi import FastAPI
from fastapi.testclient import TestClient
import json
from main import app
from routes.suite import run
from routes.suite import HTTPException
import pytest

client = TestClient(app)

def mock_run_success(args):
    return {"run": "success"}

def mock_run_failure(args):
    raise HTTPException(status_code=404)


def test_create_run(monkeypatch):
    monkeypatch.setattr("routes.suite.run", mock_run_success)
    response = client.post("/suite/", content=json.dumps({"--suite": "suite", "--user": "user"}))
    assert response.status_code == 200
    assert response.json() == {"run": {"run": "success"}}

def test_create_run_failure(monkeypatch):
    monkeypatch.setattr("routes.suite.run", mock_run_failure)
    response = client.post("/suite/", content=json.dumps({"--suite": "suite", "--user": "user"}))
    assert response.status_code == 404
