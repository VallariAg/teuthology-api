import json
import os
import sys
from base64 import b64encode
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner
from pydantic import BaseModel

from schemas.kill import KillArgs
from schemas.suite import SuiteArgs
from services.suite import make_run_name
from main import SESSION_SECRET_KEY, app

test_client = TestClient(app)


def create_mock_session_cookie(session_data) -> str:
    signer = TimestampSigner(SESSION_SECRET_KEY)

    return signer.sign(
        b64encode(json.dumps(session_data).encode("utf-8")),
    ).decode("utf-8")


mock_session_data = {
    "user": {
        "id": "mock_id",
        "username": "vallariag",
        "state": "mock_state",
        "role": "mock_role",
        "access_token": "mock_token",
    }
}

mock_session_cookie = create_mock_session_cookie(mock_session_data)

time_stamp = datetime.now()


@pytest.fixture
def mock_teuthology_suite_main(mocker):
    return mocker.patch("services.suite.teuthology.suite.main")


@pytest.fixture
def mock_teuthology_kill_main(mocker):
    return mocker.patch("services.kill.teuthology.kill.main")


@pytest.fixture
def mock_suite_get_run_details(mocker):
    return mocker.patch(
        "services.suite.get_run_details", return_value={"user": "vallariag"}
    )


@pytest.fixture
def mock_kill_get_run_details(mocker):
    return mocker.patch(
        "services.kill.get_run_details", return_value={"user": "vallariag"}
    )


@pytest.fixture
def mock_suite_logs_run(mocker):
    return mocker.patch(
        "services.suite.logs_run", return_value=["fake logs line1", "fake logs line2"]
    )


@pytest.fixture
def mock_kill_logs_run(mocker):
    return mocker.patch(
        "services.kill.logs_run", return_value=["fake logs line1", "fake logs line2"]
    )


@pytest.fixture
def mock_time_stamp(mocker):
    mocker.patch("services.suite.datetime").now.return_value = time_stamp
    return mocker.patch("services.suite.datetime").now


class CreateTestArgs:
    def __init__(self, args_model: BaseModel, correct_fields):
        self.args_model = args_model
        self.args_schema = args_model.schema()
        self.required_fields = args_model.schema()["required"]
        self.correct_fields = correct_fields

    def get_correct_fields(self):
        return {field: value for field, value in self.correct_fields.items()}

    def remove_required_fields(self):
        return {
            field: value
            for field, value in self.correct_fields.items()
            if field not in self.required_fields
        }

    def remove_non_required_fields(self):
        return {
            field: value
            for field, value in self.correct_fields.items()
            if field in self.required_fields
        }

    # def add_invalid_fields(self):
    #     pass

    # def add_incorrect_fields(self):
    #     pass


def get_run_name(route_args, mock_time_stamp):
    return make_run_name(
        {
            "machine_type": route_args.get("--machine-type", "smithi"),
            "user": route_args.get("--user"),
            "timestamp": mock_time_stamp().strftime("%Y-%m-%d_%H:%M:%S"),
            "suite": route_args.get("--suite"),
            "ceph_branch": route_args.get("--ceph", "main"),
            "kernel_branch": route_args.get("--kernel", "distro"),
            "flavor": route_args.get("--flavor", "default"),
        }
    )


mock_suite_args = {
    "--dry-run": False,
    "--non-interactive": False,
    "--verbose": 1,
    "--help": False,
    "--user": "vallariag",
    "--arch": None,
    "--ceph": "main",
    "--ceph-repo": "https://github.com/ceph/ceph-ci.git",
    "--distro": None,
    "--distro-version": None,
    "--email": None,
    "--flavor": "default",
    "--kernel": "distro",
    "--machine-type": "smithi",
    "--newest": "0",
    "--rerun-status": False,
    "--rerun-statuses": "fail,dead",
    "--sha1": None,
    "--sleep-before-teardown": "0",
    "--suite": "teuthology:no-ceph",
    "--suite-branch": None,
    "--suite-dir": None,
    "--suite-relpath": "qa",
    "--suite-repo": "https://github.com/ceph/ceph-ci.git",
    "--teuthology-branch": "main",
    "--validate-sha1": "true",
    "--wait": False,
    "<config_yaml>": [],
    "--owner": None,
    "--num": "1",
    "--priority": "70",
    "--queue-backend": None,
    "--rerun": None,
    "--seed": "-1",
    "--force-priority": False,
    "--no-nested-subset": False,
    "--job-threshold": "500",
    "--archive-upload": None,
    "--archive-upload-url": None,
    "--throttle": None,
    "--filter": None,
    "--filter-out": None,
    "--filter-all": None,
    "--filter-fragments": "false",
    "--subset": None,
    "--timeout": "43200",
    "--rocketchat": None,
    "--limit": "0",
}

mock_kill_args = {
    "--dry-run": False,
    "--non-interactive": False,
    "--verbose": 1,
    "--help": False,
    "--user": "vallariag",
    "--owner": None,
    # "--run": None,
    "--run": "fake_run",
    "--preserve-queue": None,
    "--job": None,
    "--jobspec": None,
    "--machine-type": "default",
    "--archive": None,
}


suite_test_args = CreateTestArgs(SuiteArgs, mock_suite_args)

kill_test_args = CreateTestArgs(KillArgs, mock_kill_args)
