# pylint: skip-file
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app

client = TestClient(app)


def test_v2_implements_v1():
    # Make sure the v2 endpoint has all of the v1 methods
    v1_method_list = set([route.path[len("/v1") :] for route in app.routes if route.path.startswith("/v1")])
    v2_method_list = set([route.path[len("/v2") :] for route in app.routes if route.path.startswith("/v2")])
    assert v1_method_list.intersection(v2_method_list) == v1_method_list


def test_command():
    # The v2 implementation reuses the v1 implementation, so reuse the tests also
    import test_v1_api

    test_v1_api.API_VERSION = "v2"
    test_v1_api.test_command()
    test_v1_api.test_command_failed()
