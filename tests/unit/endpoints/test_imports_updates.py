import requests

import expected_trees
from tests.unit.endpoints.difference import deep_sort_children


def test_import_and_change_parent(imports_endpoint, nodes_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [

                {
                    "id": "3fa85f64-6717-4562-b3fc-2c963f66afa6",
                    "name": "C2",
                    "type": "CATEGORY"
                },
                {
                    "id": "3fa85f64-7717-4562-b3fc-2c963f66afa6",
                    "name": "C1",
                    "type": "CATEGORY"
                },
                {
                    "id": "3fa85f64-5710-4562-b3fc-2c963f66afa6",
                    "parentId": "3fa85f64-7717-4562-b3fc-2c963f66afa6",
                    "name": "Offer 1",
                    "type": "OFFER",
                    "price": 1999
                },
                {
                    "id": "3fa85f64-5711-4562-b3fc-2c963f66afa6",
                    "parentId": "3fa85f64-6717-4562-b3fc-2c963f66afa6",
                    "name": "Offer 2",
                    "type": "OFFER",
                    "price": 1777
                }
            ],
            "updateDate": "2022-10-10T15:59:55.000Z"
        })
    assert response.status_code == 200
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "id": "3fa85f64-5710-4562-b3fc-2c963f66afa6",
                    "parentId": "3fa85f64-6717-4562-b3fc-2c963f66afa6",
                    "name": "Offer 1",
                    "type": "OFFER",
                    "price": 3000
                }
            ],
            "updateDate": "2022-12-10T15:59:55.000Z"
        })
    assert response.status_code == 200
    response = requests.get(nodes_endpoint + '3fa85f64-6717-4562-b3fc-2c963f66afa6')
    assert response.status_code == 200
    response_data = response.json()
    deep_sort_children(response_data)
    deep_sort_children(expected_trees.test_import_and_change_parent)
    assert response_data == expected_trees.test_import_and_change_parent

    response = requests.get(nodes_endpoint + '3fa85f64-7717-4562-b3fc-2c963f66afa6')
    response_data = response.json()
    deep_sort_children(response_data)
    deep_sort_children(expected_trees.test_import_and_change_parent_2)
    assert response_data == expected_trees.test_import_and_change_parent_2


def test_imports_updates_after_delete(imports_endpoint, delete_endpoint, nodes_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "id": "3fa85f64-7777-4562-b3fc-2c963f66afa6",
                    "name": "C 01",
                    "type": "CATEGORY"
                },
                {
                    "id": "3fa85f64-5710-4562-b3fc-2c973f66afa6",
                    "parentId": "3fa85f64-7777-4562-b3fc-2c963f66afa6",
                    "name": "Offer 01",
                    "type": "OFFER",
                    "price": 1999
                },
                {
                    "id": "3fa85f64-5111-4562-b3fc-2c963f76afa6",
                    "parentId": "3fa85f64-7777-4562-b3fc-2c963f66afa6",
                    "name": "Offer o2",
                    "type": "OFFER",
                    "price": 1777
                }
            ],
            "updateDate": "2022-10-15T15:00:55.000Z"
        })
    assert response.status_code == 200
    response = requests.delete(delete_endpoint + '3fa85f64-5111-4562-b3fc-2c963f76afa6')
    assert response.status_code == 200
    response = requests.delete(delete_endpoint + '3fa85f64-5710-4562-b3fc-2c973f66afa6')
    assert response.status_code == 200
    response = requests.get(nodes_endpoint + '3fa85f64-7777-4562-b3fc-2c963f66afa6')
    assert response.status_code == 200
    response_data = response.json()
    deep_sort_children(response_data)
    deep_sort_children(expected_trees.test_imports_after_delete)
    assert response_data == expected_trees.test_imports_after_delete
