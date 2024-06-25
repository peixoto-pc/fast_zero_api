import pytest
from fastapi.testclient import TestClient

from fast_zero_api.app import app


@pytest.fixture()
def client():
    return TestClient(app)
