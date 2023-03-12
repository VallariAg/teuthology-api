import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routes.suite import router

@pytest.fixture
def test_suite_route_client():
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as test_client:
        yield test_client

