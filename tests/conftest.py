import pytest


@pytest.fixture
def base_url_fixture():
    return "http://127.0.0.1:80"


@pytest.fixture
def url_fixture(base_url_fixture):
    return lambda endpoint: base_url_fixture + endpoint
