import pytest
from fastapi.testclient import TestClient
from market.api.main import app


@pytest.fixture(scope='class')
def client():
    return TestClient(app)
