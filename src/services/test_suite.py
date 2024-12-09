from fastapi.testclient import TestClient
from main import app
from suite import *

"""
Created a TestClient instance and define a dictionary run_dic with test data for the make_run_name function,
then called the function with the test data and assert that the result matches the expected output

"""

def test_make_run_name():
    client = TestClient(app)
    run_dic = {
        "user": "testuser",
        "timestamp": "2022-03-21_14:30:00",
        "suite": "test-suite",
        "ceph_branch": "ceph1",
        "kernel_branch": "kernel1",
        "flavor": "test-flavor",
        "machine_type": "test-machine"
    }
    expected_result = "testuser-2022-03-21_14:30:00-test-suite-ceph1-kernel1-test-flavor-test-machine"
    assert make_run_name(run_dic) == expected_result

"""
    Test the `make_run_name` function with an input dictionary containing a single worker machine type.
"""
def test_make_run_name_with_single_worker():
    run_dic = {
        "user": "test_user",
        "timestamp": "2022-03-21_14:30:00",
        "suite": "testing_suite",
        "ceph_branch": "ceph1",
        "kernel_branch": "kernel1",
        "flavor": "test-flavor",
        "machine_type": "worker1"
    }
    expected_run_name = "test_user-2022-03-21_14:30:00-testing_suite-ceph1-kernel1-test-flavor-worker1"
    assert make_run_name(run_dic) == expected_run_name

"""
Test the `make_run_name` function with a multi-machine type input dictionary.
"""

def test_make_run_name_with_multi_worker():
    run_dic = {
        "user": "test_user",
        "timestamp": "2022-03-21_14:30:00",
        "suite": "test-suite",
        "ceph_branch": "ceph1",
        "kernel_branch": "kernel1",
        "flavor": "test-flavor",
        "machine_type": "worker1,worker2,worker3"
    }
    expected_run_name = "test_user-2022-03-21_14:30:00-test_suite-ceph1-kernel1-test-flavor-multi"
    assert make_run_name(run_dic) == expected_run_name

"""
Test the function for no kernel branch
"""
def test_make_run_name_with_no_kernel_branch():
    run_dic = {
        "user": "teuthology",
        "timestamp": "2022-03-21_14:30:00",
        "suite": "test-suite",
        "ceph_branch": "ceph1",
        "kernel_branch": None,
        "flavor": "test-flavor",
        "machine_type": "test-machine"
    }
    expected_run_name = "teuthology-2022-03-21_14:30:00-test-suite-ceph1--test-flavor-test-machine"
    assert make_run_name(run_dic) == expected_run_name

