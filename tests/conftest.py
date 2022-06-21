import pytest


@pytest.fixture
def host():
    return 'http://127.0.0.1:8000'


@pytest.fixture
def imports_endpoint(host):
    return host + "/imports"


@pytest.fixture
def delete_endpoint(host):
    return host + "/delete/"


@pytest.fixture
def nodes_endpoint(host):
    return host + "/nodes/"
