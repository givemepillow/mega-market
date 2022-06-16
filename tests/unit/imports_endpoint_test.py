import pytest
import requests


@pytest.fixture
def endpoint():
    return "/imports"


class TestValidRequestsToImportsEndpoint:

    def test_valid_post_1(self, endpoint, client):
        response = client.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Товары",
                        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 200

    def test_valid_post_2(self, endpoint, client):
        response = client.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Смартфоны",
                        "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                    },
                    {
                        "type": "OFFER",
                        "name": "jPhone 13",
                        "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                        "price": 79999
                    },
                    {
                        "type": "OFFER",
                        "name": "Xomiа Readme 10",
                        "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                        "price": 59999
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200

    def test_valid_post_3(self, endpoint, client):
        response = client.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Телевизоры",
                        "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                    },
                    {
                        "type": "OFFER",
                        "name": "Samson 70\" LED UHD Smart",
                        "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 32999
                    },
                    {
                        "type": "OFFER",
                        "name": "Phyllis 50\" LED UHD Smarter",
                        "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 49999
                    }
                ],
                "updateDate": "2022-02-03T12:00:00.000Z"
            }
        )
        assert response.status_code == 200

    def test_valid_post_4(self, endpoint, client):
        response = client.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Goldstar 65\" LED UHD LOL Very Smart",
                        "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 69999
                    }
                ],
                "updateDate": "2022-06-13T03:06:22+00:00"
            }
        )
        assert response.status_code == 200


class TestInvalidRequestsToImportsEndpoint:
    def test_non_uuid_id(self, endpoint, client):
        response = client.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Товары",
                        "id": "bbdd-47d3-ad8f",
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_int_id(self, endpoint, client):
        response = client.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Товары",
                        "id": 1000,
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_invalid_type(self, endpoint, client):
        response = client.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "SOMETHING",
                        "name": "Товары",
                        "id": 1000,
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }
