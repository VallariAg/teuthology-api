from conftest import (SuiteArgs, get_run_name, mock_session_cookie,
                      mock_suite_get_run_details, mock_suite_logs_run,
                      mock_teuthology_suite_main, mock_time_stamp,
                      suite_test_args, test_client)


def test_suite(mock_teuthology_suite_main, mock_suite_get_run_details, mock_time_stamp):
    """
    Test creating a run with valid and correct input
    """
    request_body = suite_test_args.get_correct_fields()
    test_client.cookies = {"session": mock_session_cookie}

    response = test_client.post("/suite", json=request_body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    expected_fields = {"run": dict, "logs": list}  # {"run": run_details, "logs": []}
    for field, type in expected_fields.items():
        assert field in response.json()
        assert isinstance(response.json()[field], type)

    assert response.json()["logs"] == []

    expected_run_name = get_run_name(request_body, mock_time_stamp)
    mock_suite_get_run_details.assert_called_once_with(expected_run_name)
    request_body["--timestamp"] = mock_time_stamp().strftime("%Y-%m-%d_%H:%M:%S")
    mock_teuthology_suite_main.assert_called_once_with(request_body)


def test_suite_missing_required_fields():
    """
    Test creating a run without required fields
    """
    request_body = suite_test_args.remove_required_fields()
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.post("/suite", json=request_body)

    assert response.status_code == 422
    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)

    required_fields = SuiteArgs.schema()["required"]
    for index, field in enumerate(required_fields):
        assert field in response.json()["detail"][index]["loc"]
        assert "body" in response.json()["detail"][index]["loc"]
        assert response.json()["detail"][index]["msg"] == "field required"
        assert response.json()["detail"][index]["type"] == "value_error.missing"

    assert len(response.json()["detail"]) == len(required_fields)


def test_suite_missing_non_required_fields(
    mock_teuthology_suite_main, mock_suite_get_run_details, mock_time_stamp
):
    """
    Test creating a run without non-required fields
    """
    request_body = suite_test_args.remove_non_required_fields()
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.post("/suite", json=request_body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    expected_fields = {"run": dict, "logs": list}  # {"run": run_details, "logs": []}
    for field, type in expected_fields.items():
        assert field in response.json()
        assert isinstance(response.json()[field], type)

    assert response.json()["logs"] == []

    expected_run_name = get_run_name(request_body, mock_time_stamp)
    mock_suite_get_run_details.assert_called_once_with(expected_run_name)
    request_body["--timestamp"] = mock_time_stamp().strftime("%Y-%m-%d_%H:%M:%S")
    request_body.update(suite_test_args.get_correct_fields())
    mock_teuthology_suite_main.assert_called_once_with(request_body)


# def test_suite_invalid_fields():
#     """
#     Test creating a run with invalid input
#     """
#     request_body = {}
#     test_client.cookies = {"session": mock_session_cookie}
#     response = test_client.post("/suite", json=request_body)

#     assert response.status_code == 422
#     assert isinstance(response.json(), dict)

#     expected_fields = ["detail"]
#     for field in expected_fields:
#         assert field in response.json()

#     assert "value is not a valid string" in response.json()["detail"][0]["msg"]


# def test_suite_incorrect_fields():
#     """
#     Test creating a run with incorrect input
#     """
#     request_body = {}
#     test_client.cookies = {"session": mock_session_cookie}
#     response = test_client.post("/suite", json=request_body)

#     assert response.status_code == 500
#     assert isinstance(response.json(), dict)

#     expected_fields = {}
#     for field in expected_fields:
#         assert field in response.json()


def test_suite_dry_run(
    mock_teuthology_suite_main,
    mock_suite_get_run_details,
    mock_suite_logs_run,
    mock_time_stamp,
):
    """
    Test creating a run with dry run
    """
    request_body = suite_test_args.get_correct_fields()
    request_body["--dry-run"] = True
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.post("/suite?dry_run=True", json=request_body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    expected_fields = {"run": dict, "logs": list}  # {"run": {}, "logs": logs}
    for field, type in expected_fields.items():
        assert field in response.json()
        assert isinstance(response.json()[field], type)

    assert response.json()["run"] == {}
    assert response.json()["logs"] != []

    request_body["--timestamp"] = mock_time_stamp().strftime("%Y-%m-%d_%H:%M:%S")
    mock_suite_logs_run.assert_called_once_with(
        mock_teuthology_suite_main, request_body
    )


def test_suite_logs(
    mock_teuthology_suite_main,
    mock_suite_get_run_details,
    mock_suite_logs_run,
    mock_time_stamp,
):
    """
    Test creating a run with logs
    """
    request_body = suite_test_args.get_correct_fields()
    test_client.cookies = {"session": mock_session_cookie}
    response = test_client.post("/suite?logs=True", json=request_body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    expected_fields = {"run": dict, "logs": list}  # {"run": run_details, "logs": logs}
    for field, type in expected_fields.items():
        assert field in response.json()
        assert isinstance(response.json()[field], type)

    assert response.json()["logs"] != []

    expected_run_name = get_run_name(request_body, mock_time_stamp)
    mock_suite_get_run_details.assert_called_once_with(expected_run_name)

    request_body["--timestamp"] = mock_time_stamp().strftime("%Y-%m-%d_%H:%M:%S")
    mock_suite_logs_run.assert_called_once_with(
        mock_teuthology_suite_main, request_body
    )


def test_suite_logged_out():
    """
    Test creating a run while logged out
    """
    request_body = suite_test_args.get_correct_fields()
    test_client.cookies = {}
    response = test_client.post("/suite?dry_run=True", json=request_body)

    assert response.status_code == 401
    assert isinstance(response.json(), dict)
    assert response.json() == {"detail": "You need to be logged in"}
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == "Bearer"
