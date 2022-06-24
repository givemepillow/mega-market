import pytest
import requests


@pytest.fixture
def endpoint(host):
    return host + "/delete/"


class TestInvalidRequestsToDeleteEndpoint:
    def test_delete_non_exists_unit(self, endpoint):
        response = requests.delete(
            endpoint + "c27d3e8e-1f14-4525-97c5-2f965a89ae57"
        )
        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Item not found"
        }

    def test_invalid_uuid_1(self, endpoint):
        response = requests.delete(
            endpoint + "c27d3e8e-1f14-45025-97c5-2f965a89ae57"
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_invalid_uuid_2(self, endpoint):
        response = requests.delete(
            endpoint + "unit"
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }
