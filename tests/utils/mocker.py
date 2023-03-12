import pytest

def mock_response(mocker,target,response):
    mocker.patch(target,return_value=response)

def mock_exception(mocker,target,result):
    mocker.patch(target,side_effect=result)