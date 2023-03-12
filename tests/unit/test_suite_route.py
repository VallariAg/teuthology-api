from ..utils.mocker import mock_exception,mock_response

def test_run_success(mocker, test_suite_route_client):
    mock_response(mocker, "src.routes.suite.run", { "run": "success", "logs": "log" })
    response= test_suite_route_client.post('/suite',json={"--suite":"suite","--user":"user"})
    assert response.status_code == 200
    assert response.json() == { "run": "success", "logs": "log" }

def test_incorrect_args(mocker, test_suite_route_client):
    mock_response(mocker, "src.routes.suite.run", { "run": "success", "logs": "log" })
    response= test_suite_route_client.post('/suite',json={"--s":"suite","--u":"user"})
    assert response.status_code == 422

def test_run_failure(mocker, test_suite_route_client):
    mock_exception(mocker,"src.routes.suite.run", Exception("run_error"))
    response= test_suite_route_client.post('/suite',json={"--suite":"suite","--user":"user"})
    assert response.status_code == 404