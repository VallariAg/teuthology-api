def test_git_login(test_client):
    response = test_client.get("/login")
    assert response.status_code == 302
