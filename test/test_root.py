import os, sys
from fastapi.testclient import TestClient
from fastapi import status

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),"src"))
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"root": "success"}