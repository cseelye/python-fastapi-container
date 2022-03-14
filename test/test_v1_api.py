# pylint: skip-file
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app

client = TestClient(app)


# See https://fastapi.tiangolo.com/tutorial/testing/ for more inspiration


API_VERSION = "v1"


def test_about():
    response = client.get(f"/{API_VERSION}/about")
    assert response.status_code == 200
    assert response.json()["service_name"] == "TemplateService"
    if Path("/version").exists():
        assert response.json()["version"] == Path("/version").read_text(encoding="utf-8").strip()
    else:
        assert response.json()["version"] == "99.99.99"


def test_command():
    response = client.post(f"/{API_VERSION}/command", json={"commandline": "pwd"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["return_code"] == 0
    assert response.json()["stderr"].strip() == ""
    assert response.json()["stdout"].strip() == "/"
    assert response.json()["elapsed_time"] < 0.25


def test_command_failed():
    response = client.post(f"/{API_VERSION}/command", json={"commandline": "false"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["return_code"] == 1
    assert response.json()["stderr"].strip() == ""
    assert response.json()["stdout"].strip() == ""
    assert response.json()["elapsed_time"] < 0.25
