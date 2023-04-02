from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import datetime
#import teuthology.suite
from suite import run, make_run_name
from fastapi import HTTPException
from main import app

client = TestClient(app)

def test_create_run_with_valid_input():
    suite_args = {
        "--suite": "test-suite",
        "--ceph": "ceph-version",
        "--kernel": "kernel-version",
        "--flavor": "flavor",
        "--machine-type": "machine-type",
        "--user": "user"
    }
    access_token = "valid-access-token"
    dry_run = False
    logs = True
    expected_run_name = "user-{}-test-suite-ceph-version-kernel-version-flavor-machine-type".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    
    #C:\Users\HP\Documents\docker\teuthology-api\src\services\test_suite.py
    with patch("services.suite.teuthology.suite.main") as mock_teuthology_suite_main, \
         patch("services.suite.get_run_details") as mock_get_run_details, \
         patch("services.suite.logs_run") as mock_logs_run:
        mock_logs_run.return_value = ["log line 1", "log line 2"]
        mock_get_run_details.return_value = {"run": "details"}
        response = client.post(
            "/suite/",
            json=suite_args,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"dry_run": dry_run, "logs": logs}
        )

    assert response.status_code == 200
    assert response.json() == {"run": {"run": "details"}, "logs": ["log line 1", "log line 2"]}
    mock_teuthology_suite_main.assert_called_once_with(suite_args)
    mock_logs_run.assert_called_once_with(teuthology.suite.main, suite_args)
    mock_get_run_details.assert_called_once_with(expected_run_name)

def test_create_run_with_missing_access_token():
    suite_args = {
        "--suite": "test-suite",
        "--ceph": "ceph-version",
        "--kernel": "kernel-version",
        "--flavor": "flavor",
        "--machine-type": "machine-type",
        "--user": "user"
    }
    access_token = ""
    dry_run = False
    logs = True

    response = client.post(
        "/suite/",
        json=suite_args,
        headers={"Authorization": f"Bearer {access_token}"},
        params={"dry_run": dry_run, "logs": logs}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "You need to be logged in"}
    assert response.headers["WWW-Authenticate"] == "Bearer"

def test_create_run_with_teuthology_error():
    suite_args = {
        "--suite": "test-suite",
        "--ceph": "ceph-version",
        "--kernel": "kernel-version",
        "--flavor": "flavor",
        "--machine-type": "machine-type",
        "--user": "user"
    }
    access_token = "valid-access-token"
    dry_run = False
    logs = True

    with patch("services.suite.teuthology.suite.main") as mock_teuthology_suite_main:
        mock_teuthology_suite_main.side_effect = Exception("teuthology error")
        response = client.post(
            "/suite/",
            json=suite_args,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"dry_run": dry_run, "logs": logs}
        )

    assert response.status_code == 500
   
