import json

import expected_trees

import requests


def test_import_and_nodes(imports_endpoint, delete_endpoint, nodes_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "type": "OFFER",
                    "name": "Teapot 1",
                    "id": "f2e29f8c-9cca-4bf9-8021-0a1878225680",
                    "price": 1999,
                    "parentId": None
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 2",
                    "id": "53c9a389-4061-4119-a5d2-98dd0a565034",
                    "price": 1999,
                    "parentId": None
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 3",
                    "id": "885f4ee7-bcc9-49a9-886f-9b4420b6d9f0",
                    "price": 1999,
                    "parentId": None
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 4",
                    "id": "9cc7228e-847f-40a8-9d3f-6d9c058303a4",
                    "price": 1999,
                    "parentId": None
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 5",
                    "id": "674b1399-8168-4a69-a1c3-9cddd610867d",
                    "price": 1999,
                    "parentId": None
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 6",
                    "id": "9e217f61-e9e5-4cb9-a43f-0fe4b6aa0caa",
                    "price": 1999,
                    "parentId": "bec234c4-5ad9-4f65-b684-82b2efa7ced1"
                },

            ],
            "updateDate": "2024-02-10T12:00:00.000Z"
        }

    )
    assert response.status_code == 400
    response = requests.get(
        nodes_endpoint + "f2e29f8c-9cca-4bf9-8021-0a1878225680"
    )
    assert response.status_code == 404
    response = requests.get(
        nodes_endpoint + "674b1399-8168-4a69-a1c3-9cddd610867d"
    )
    assert response.status_code == 404


def test_average_price(imports_endpoint, delete_endpoint, nodes_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "First",
                    "id": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
                    "parentId": None
                },
                {
                    "type": "CATEGORY",
                    "name": "SECOND 1",
                    "id": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
                    "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9"
                },
                {
                    "type": "CATEGORY",
                    "name": "SECOND 2",
                    "id": "fb53fa86-dd6f-4f30-b57c-579576b78384",
                    "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9"
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 1",
                    "id": "7443a5a2-f31d-4dab-94c0-a7857ed6437f",
                    "price": 1200,
                    "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9"
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 2 1",
                    "id": "c0cd0e5c-89ee-4db3-9b40-1045abd42182",
                    "price": 600,
                    "parentId": "18df93bd-86c4-4c90-913b-0c0f897b6df6"
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 2 2",
                    "id": "cb45dfa2-f31c-4900-a109-a13dc4a8d27b",
                    "price": 770,
                    "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384"
                },
                {
                    "type": "OFFER",
                    "name": "Teapot 2 3",
                    "id": "cb45dfa2-f31c-4900-a119-a13dc4a8d27b",
                    "price": 120,
                    "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384"
                }

            ],
            "updateDate": "2022-01-05T12:00:00.000Z"
        }

    )
    assert response.status_code == 200
    response = requests.get(
        nodes_endpoint + "19a0a478-6a57-4f44-a2fe-0c21fb1746e9"
    )
    assert response.json() == expected_trees.test_average_price


def test_average_price_after_delete_offer(imports_endpoint, delete_endpoint, nodes_endpoint):
    response = requests.delete(delete_endpoint + "cb45dfa2-f31c-4900-a119-a13dc4a8d27b")
    assert response.status_code == 200
    response = requests.get(
        nodes_endpoint + "19a0a478-6a57-4f44-a2fe-0c21fb1746e9"
    )
    assert response.json() == expected_trees.test_average_price_after_delete_offer


def test_average_price_and_date_after_replace_category(imports_endpoint, delete_endpoint, nodes_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "id": "fb53fa86-dd6f-4f30-b57c-579576b78384",
                    "type": "CATEGORY",
                    "name": "SECOND 2",
                    "parentId": "18df93bd-86c4-4c90-913b-0c0f897b6df6"
                },
                {
                    "id": "c0cd0e5c-89ee-4db3-9b40-1045abd42182",
                    "type": "OFFER",
                    "name": "Teapot 2 1",
                    "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384",
                    "price": 600
                }
            ],
            "updateDate": "2022-06-21T01:41:40.716Z"
        }
    )
    assert response.status_code == 200
    response = requests.get(
        nodes_endpoint + "19a0a478-6a57-4f44-a2fe-0c21fb1746e9"
    )
    assert response.json() == expected_trees.test_average_price_and_date_after_replace_category


def test_delete_and_update_offer_price(imports_endpoint, delete_endpoint, nodes_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "id": "7443a5a2-f31d-4dab-94c0-a7857ed6437f",
                    "type": "OFFER",
                    "name": "Teapot 1",
                    "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
                    "price": 0
                }
            ],
            "updateDate": "2022-06-21T01:56:40.716Z"
        }
    )
    assert response.status_code == 200
    response = requests.delete(delete_endpoint + "c0cd0e5c-89ee-4db3-9b40-1045abd42182")
    assert response.status_code == 200
    response = requests.delete(delete_endpoint + "cb45dfa2-f31c-4900-a109-a13dc4a8d27b")
    assert response.status_code == 200
    response = requests.get(
        nodes_endpoint + "19a0a478-6a57-4f44-a2fe-0c21fb1746e9"
    )
    assert response.json() == expected_trees.test_delete_and_update_offer_price
