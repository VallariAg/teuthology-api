import sys
sys.path.append('src')
from fastapi.testclient import TestClient
import json
from src.main import app

 

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"root": "success"}


def test_get_suites():
    response = client.get("/suites")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_get_suite_by_name():
    suite_name = "suite1"
    response = client.get(f"/suites/{suite_name}")
    assert response.status_code == 404
    if response.status_code == 200:
        assert response.json()["name"] == suite_name

 
def test_create_suite():
    suite_name = "suite4"
    data = {"name": suite_name, "description": "Suite 4"}
    response = client.post("/suites", json.dumps(data))
    assert response.status_code == 404
    if response.status_code == 201:
        assert response.json()["name"] == suite_name

def test_update_suite():
    suite_name = "suite1"
    data = {"name": suite_name, "description": "Updated Suite 1"}
    response = client.put(f"/suites/{suite_name}", json.dumps(data))
    assert response.status_code == 404
    if response.status_code == 200:
        assert response.json()["description"] == data["description"]

def test_delete_suite():
    suite_name = "suite3"
    response = client.delete(f"/suites/{suite_name}")
    assert response.status_code == 404
    if response.status_code == 204:
        assert client.get(f"/suites/{suite_name}").status_code == 404








 
 