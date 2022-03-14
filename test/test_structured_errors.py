# pylint: skip-file
"""
Test that all errors from the API match out structured error specification
"""
from fastapi import APIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import app
from app.exceptions import AppException

client = TestClient(app)


# Create a new endpoint that throws verious errors so we can test the response returned to the client
error_router = APIRouter(prefix="/asdf-test")


class InputModel(BaseModel):
    stringy: str
    inty: int


EXCEPTION_MESSAGE = "Application error during API call"
EXCEPTION_CODE = 123
EXCEPTION_DETAIL = {"key": "value", "nested": {"morekey": "morevalue"}, "list": [1, 2, 3]}


@error_router.post("/error")
async def error_endpoint(param: InputModel):
    raise AppException(EXCEPTION_MESSAGE, code=EXCEPTION_CODE, detail=EXCEPTION_DETAIL)


app.include_router(error_router)


# Test that HTTP errors come back in our format
def test_api_not_allowed():
    response = client.get("/asdf-test/error")
    print(response.json())
    assert response.status_code == 405
    assert set(response.json().keys()) == set(["message", "errorCode", "detail"])
    assert response.json()["message"] == "Method Not Allowed"
    assert response.json()["errorCode"] == 4


def test_api_not_found():
    response = client.get("/asdf-test/nonexistant")
    print(response.json())
    assert response.status_code == 404
    assert set(response.json().keys()) == set(["message", "errorCode", "detail"])
    assert response.json()["message"] == "Not Found"
    assert response.json()["errorCode"] == 4


# Test that validation errors come back in our format
def test_api_validation_error():
    # Invalid values
    response = client.post("/asdf-test/error", json={"stringy": "ss", "inty": "zz"})
    print(response.json())
    assert response.status_code == 422
    assert set(response.json().keys()) == set(["message", "errorCode", "detail"])
    assert response.json()["message"].startswith("Request Validation Error: ")
    assert response.json()["errorCode"] == 1
    assert ".".join(response.json()["detail"]["error"][0]["loc"]) == "body.inty"
    assert response.json()["detail"]["error"][0]["msg"] == "value is not a valid integer"

    # Plain text
    response = client.post("/asdf-test/error", data="asdf")
    print(response.json())
    assert response.status_code == 422
    assert set(response.json().keys()) == set(["message", "errorCode", "detail"])
    assert response.json()["message"].startswith("Request Validation Error: ")
    assert response.json()["errorCode"] == 1


# Test that application errors come back in our format
def test_api_application_error():
    response = client.post("/asdf-test/error", json={"stringy": "asdf", "inty": 1})
    print(response.json())
    assert response.status_code == 500
    assert set(response.json().keys()) == set(["message", "errorCode", "detail"])
    assert response.json()["message"] == EXCEPTION_MESSAGE
    assert response.json()["errorCode"] == EXCEPTION_CODE
    assert response.json()["detail"] == EXCEPTION_DETAIL
