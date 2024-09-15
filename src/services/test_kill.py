import unittest
from unittest import mock
from unittest.mock import patch
from fastapi import FastAPI
from fastapi import Request,HTTPException
from fastapi.testclient import TestClient
from helpers import logs_run, get_username, get_run_details
#from config import settings
#import teuthology.kill
from kill import run
from main import app

 # test a successful kill job
def test_run_success():
    client = TestClient(app)
    access_token = "valid_token"
    args = {"--run": "12345"}
    send_logs = False
    request = client.post("/kill")
    
    with patch("services.kill.teuthology.kill.main") as mock_kill:
        response = run(args, send_logs, access_token, request)
        mock_kill.assert_called_once_with(args)
    
    assert response == {"kill": "success"}

# test missing token 
def test_missing_accesstoken():
    client = TestClient(app)
    access_token = ""
    args = {"--run": "12345"}
    send_logs = False
    request = client.post("/kill")
    with patch("services.kill.teuthology.kill.main"):
        response = run(args, send_logs, access_token, request)
    
    assert response.status_code == 401
    #assert response.headers == {"WWW-Authenticate": "Bearer"}

# test missing run name 
def test_run_missing_run_name():
    client = TestClient(app)
    access_token = "valid_token"
    args = {}
    send_logs = False
    request = client.post("/kill")
    
    with patch("services.kill.teuthology.kill.main"):
        response = run(args, send_logs, access_token, request)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "--run is a required argument"}


def test_run_user_not_authorized():
    client = TestClient(app)
    access_token = "valid_token"
    args = {"--run": "12345"}
    send_logs = False
    request = client.post("/kill")
    
    with patch("services.kill.get_username") as mock_username:
        mock_username.return_value = "user1"
        with patch("services.kill.get_run_details") as mock_run_details:
            mock_run_details.return_value = {"user": "user2"}
            response = run(args, send_logs, access_token, request)
    
    assert response.status_code == 401
    assert response.json() == {"detail": "You don't have permission to kill this run/job"}    

def test_run_teuthology_exception():
    client = TestClient(app)
    access_token = "valid_token"
    args = {"--run": "12345"}
    send_logs = False
    request = client.post("/kill")
    
    with patch("services.kill.teuthology.kill.main") as mock_kill:
        mock_kill.side_effect = Exception("some error")
        response = run(args, send_logs, access_token, request)
    
    assert response.status_code == 500
    assert response.json() == {"detail": "Exception('some error',)"}






