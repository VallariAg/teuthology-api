mock_kill_args = {
    "--dry-run": False,
    "--non-interactive": False,
    "--verbose": 1,
    "--help": False,
    "--user": "mock_user",
    "--owner": None,
    "--run": "mock_run",
    "--preserve-queue": None,
    "--job": None,
    "--jobspec": None,
    "--machine-type": "testnode",
    "--archive": None,
}


def test_kill_no_auth(test_client):
    response = test_client.post("/kill")
    assert response.status_code == 401
    assert response.json() == {"detail": "You need to be logged in"}
