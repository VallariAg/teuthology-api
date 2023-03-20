import os, sys
from fastapi.testclient import TestClient
from fastapi import status

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),"src"))
from main import app

client = TestClient(app)

# Test that default options get passed for us with minimal options
def test_default_args():
    minimal_options = {
        "--ceph": "wip-dis-testing-2",
        "--limit": "2",
        "--machine-type": "testnode",
        "--suite": "teuthology:no-ceph",
        "--suite-branch": "wip-dis-testing-2",
        "--user": "vallariag"
    }
    response = client.post("/suite?dry_run=true&logs=true", json=minimal_options)
    json_response = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json_response["run"] == {} # Assert that run is empty because we perform a dry run
    assert len(json_response["logs"]) > 0 # Assert that we receive logs in our response

# Test that we get a 200 response with correct options
def test_correct_args():
    correct_options = {
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
    response = client.post("/suite?dry_run=true&logs=true", json=correct_options)
    json_response = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json_response["run"] == {} # Assert that run is empty because we perform a dry run
    assert len(json_response["logs"]) > 0 # Assert that we receive logs in our response

# Test that we get a 400 response with incorrect options
def test_incorrect_args():
    incorrect_options = {
        "--ceph": "piw-dis-testing-2", #incorrect (changed wip to piw)
        "--ceph-repo": "https://github.com/cep/cep-ci.git", #incorrect (changed ceph to cep)
        "--kernel": "astro", #incorrect (changed distro to astro)
        "--limit": "2",
        "--newest": "0",
        "--machine-type": "testnode",
        "--num": "1",
        "--priority": "70",
        "--suite": "teuthology:no-cep", #incorrect (changed ceph to cep)
        "--suite-branch": "piw-dis-testing-2", #incorrect (changed wip to piw)
        "--suite-repo": "https://github.com/cep/cep-ci.git", #incorrect (changed ceph to cep)
        "--teuthology-branch": "man", #incorrect (changed main to man)
        "--verbose": "1",
        "--user": "vallariag"
    }
    response = client.post("/suite?dry_run=false&logs=true", json=incorrect_options)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Test that we get a 422 response with invalid options
def test_invalid_args():
    invalid_options = {
        "--ceph": "wip-dis-testing-2",
        "--ceph-repo": "https://github.com/ceph/ceph-ci.git",
        "--kernel": [], #invalid (should be type string)
        "--limit": "2",
        "--newest": "0",
        "--machine-type": "testnode",
        "--num": "1",
        "--priority": {}, #invalid (should be type string)
        "--suite": "teuthology:no-ceph",
        "--suite-branch": "wip-dis-testing-2",
        "--suite-repo": [], #invalid (should be type string)
        "--teuthology-branch": "main",
        "--verbose": "1",
        "--user": "vallariag"
    }
    response = client.post("/suite?dry_run=false&logs=true", json=invalid_options)
    json_response = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(json_response["detail"]) == 3 # Assert that it matches the number of invalid options above
    # Assert that the names of invalid options matches with above
    assert json_response["detail"][0]["loc"][1] == "--kernel"
    assert json_response["detail"][1]["loc"][1] == "--suite-repo"
    assert json_response["detail"][2]["loc"][1] == "--priority"