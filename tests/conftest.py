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


@pytest.fixture
def sales_endpoint(host):
    return host + "/sales/"


@pytest.fixture
def statistic_endpoint(host):
    return lambda _id: host + "/node/" + _id + "/statistic"


@pytest.fixture
def sort():
    def sort_children(node):
        if node.get("children"):
            node["children"].sort(key=lambda x: x["id"])

            for child in node["children"]:
                sort_children(child)

    return sort_children
