def test_suite_no_auth(test_client):
    response = test_client.post("/suite")
    assert response.status_code == 401
    assert response.json() == {"detail": "You need to be logged in"}
