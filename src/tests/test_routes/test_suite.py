def test_create_suite(test_client, suite_payload):
    response = test_client.post(
        "/suite",
        headers={"Content-Type": "application/json"},
        params={"dry_run": False, "logs":True},
        json=suite_payload,
    )
    assert response.status_code == 200
    assert response.get("run") == {} 
    assert len(response.get("logs")) > 0 


def test_failed_create_suite(test_client, suite_payload):
    response = test_client.post(
        "/suite",
        headers={"Content-Type": "application/json"},
        params={"dry_run": False, "logs":True},
        json=suite_payload,
    )
    assert response.status_code == 401   


