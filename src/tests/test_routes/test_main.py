

def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json().get("root") ==  "success"
    assert len(response.json()) ==  2