from conftest import (KillArgs, kill_test_args, mock_kill_get_run_details,
                      mock_kill_logs_run, mock_session_cookie,
                      mock_teuthology_kill_main, test_client)


def test_kill(mock_kill_get_run_details, mock_teuthology_kill_main):
    """
    Test killing a run with valid and correct input
    """
    request_body = kill_test_args.get_correct_fields()
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.post("/kill", json=request_body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    expected_fields = {"kill": str}  # {"kill": "success"}
    for field, type in expected_fields.items():
        assert field in response.json()
        assert isinstance(response.json()[field], type)

    assert response.json() == {"kill": "success"}

    mock_kill_get_run_details.assert_called_once_with(request_body["--run"])
    mock_teuthology_kill_main.assert_called_once_with(request_body)


# def test_kill_missing_required_fields(mock_kill_get_run_details):
#     """
#     Test killing a run without required fields
#     """
#     request_body = kill_test_args.remove_required_fields()
#     test_client.cookies = {"session": mock_session_cookie}
#     response = test_client.post("/kill", json=request_body)

#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert isinstance(response.json()["detail"], list)

#     required_fields = KillArgs.schema()["required"]
#     for index, field in enumerate(required_fields):
#         assert field in response.json()["detail"][index]["loc"]
#         assert "body" in response.json()["detail"][index]["loc"]
#         assert response.json()["detail"][index]["msg"] == "field required"
#         assert response.json()["detail"][index]["type"] == "value_error.missing"

#     assert len(response.json()["detail"]) == len(required_fields)


def test_kill_missing_non_required_fields(mock_kill_get_run_details):
    """
    Test killing a run without non-required fields
    """
    request_body = kill_test_args.remove_non_required_fields()
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.post("/kill", json=request_body)

    assert response.status_code == 400
    assert isinstance(response.json(), dict)
    assert response.json() == {"detail": "--run is a required argument"}


# def test_kill_invalid_fields(mock_kill_get_run_details):
#     """
#     Test killing a run with invalid input
#     """
#     request_body = {}
#     test_client.cookies = {"session": mock_session_cookie}
#     response = test_client.post("/kill", json=request_body)

#     assert response.status_code == 422
#     assert isinstance(response.json(), dict)

#     expected_fields = ["detail"]
#     for field in expected_fields:
#         assert field in response.json()

#     assert "value is not a valid string" in response.json()["detail"][0]["msg"]


# def test_kill_incorrect_fields(mock_kill_get_run_details):
#     """
#     Test killing a run with incorrect input
#     """
#     request_body = {}
#     test_client.cookies = {"session": mock_session_cookie}
#     response = test_client.post("/kill", json=request_body)

#     assert response.status_code == 500
#     assert isinstance(response.json(), dict)

#     expected_fields = {}
#     for field in expected_fields:
#         assert field in response.json()


def test_kill_logs(
    mock_kill_get_run_details, mock_kill_logs_run, mock_teuthology_kill_main
):
    """
    Test killing a run with logs
    """
    request_body = kill_test_args.get_correct_fields()
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.post("/kill?logs=True", json=request_body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    expected_fields = {"logs": list}  # {"logs": logs}
    for field, type in expected_fields.items():
        assert field in response.json()
        assert isinstance(response.json()[field], type)

    assert response.json()["logs"] != []

    mock_kill_logs_run.assert_called_once_with(mock_teuthology_kill_main, request_body)


def test_kill_logged_out():
    """
    Test killing a run while logged out
    """
    request_body = kill_test_args.get_correct_fields()
    test_client.cookies = {}
    response = test_client.post("/kill", json=request_body)

    assert response.status_code == 401
    assert isinstance(response.json(), dict)
    assert response.json() == {"detail": "You need to be logged in"}
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == "Bearer"
