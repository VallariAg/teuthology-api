import pytest
from fastapi.testclient import TestClient
from schemas.base import BaseArgs
from schemas.schedule import SchedulerArgs
from schemas.suite import SuiteArgs
from schemas.kill import KillArgs


from main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    create test client instance
    """
    client = TestClient(app)
    yield client  


@pytest.fixture(scope="module")
def suite_payload() -> dict:
    """
    create test client instance
    """
    payload = {
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
    
    return payload 


@pytest.fixture(scope="module")
def base_schema_payload() -> tuple:
    payload: dict = {
            "--dry-run":True,
            "--non-interactive":True,
            "--verbose":1,
            "--help":True,
            "--user":"vallariag"
    }

    return (payload, BaseArgs )


@pytest.fixture(scope="module")
def schedule_schema_payload() -> tuple:
    payload: dict = {
        "--owner":"vallariag",
        "--seed":"-4",
        "--force-priority":True,
        "--no-nested-subset":True,
        "--job-threshold":"627",
    }
    
    return (payload, SchedulerArgs)




@pytest.fixture(scope="module")
def suite_schema_payload() -> tuple:
    payload: dict = {
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
    return (payload, SuiteArgs)


@pytest.fixture(scope="module")
def kill_schema_payload() -> tuple:
    payload: dict = {
      
        "--run": "run job",
        "--preserve-queue": True,
        "--job": ["job1", "job2"],
        "--jobspec": "do job",
        "--machine-type": "debian",
        "--archive": "",
        "--user": "vallariag",
        "--dry-run": False,
    }
     
    return (payload, KillArgs)
