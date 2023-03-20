import pytest
from starlette.testclient import TestClient

from main import create_app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app=create_app()) as client:
        yield client
