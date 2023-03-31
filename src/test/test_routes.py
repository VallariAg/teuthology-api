from main import app
from services.helpers import get_token
from test.conftest import mock_get_token


def test_suite_create_run(archive_dir, test_client):
    app.dependency_overrides[get_token] = mock_get_token
    response = test_client.post(
        "/suite",
        headers={"Content-Type": "application/json"},
        params={"dry_run": False, "logs": True},
        json={
            "--ceph": "wip-dis-testing-2",
            "--ceph-repo": "https://github.com/ceph/ceph-ci.git",
            "--kernel": "distro",
            "--limit": "2",
            "--newest": "0",
            "--machine-type": "testnode",
            "--num": "1",
            "--priority": "70",
            "--suite": "teuthology:no-ceph",
            "--suite-branch": "wip-dis-testing-2",
            "--suite-repo": "https://github.com/ceph/ceph-ci.git",
            "--teuthology-branch": "main",
            "--verbose": "1",
            "--user": "vallariag"
        }
    )
    assert response.status_code == 200
    assert response.json()[0].get("run") == {}
    assert len(response.get("logs")) > 0
