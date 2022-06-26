import requests


def test_sales_for_offer_in_24(imports_endpoint, delete_endpoint, sales_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "id": "7e72d177-7730-4b0d-9cba-499c515715ad",
                    "name": "Машина%:?*()",
                    "type": "OFFER",
                    "price": 1000000
                },
                {
                    "id": "adcc7c57-a8a7-4ed8-a5ce-d710f183b05f",
                    "name": "'НЕ'\n\n\n Машина%:?*()",
                    "type": "OFFER",
                    "price": 0
                }
            ],
            "updateDate": "2022-06-30T07:15:00.000Z"
        }
    )
    assert response.status_code == 200
    response = requests.get(
        sales_endpoint,
        params={"date": "2022-06-30T07:15:00.000Z"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "7e72d177-7730-4b0d-9cba-499c515715ad",
                "name": "Машина%:?*()",
                "parentId": None,
                "type": "OFFER",
                "price": 1000000,
                "date": "2022-06-30T07:15:00.000Z"
            },
            {
                "id": "adcc7c57-a8a7-4ed8-a5ce-d710f183b05f",
                "name": "'НЕ'\n\n\n Машина%:?*()",
                "parentId": None,
                "type": "OFFER",
                "price": 0,
                "date": "2022-06-30T07:15:00.000Z"
            }
        ]
    }
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "id": "adcc7c57-a8a7-4ed8-a5ce-d710f183b05f",
                    "name": "Машина.",
                    "type": "OFFER",
                    "price": 20000000
                }
            ],
            "updateDate": "2022-06-31T07:15:00.000Z"
        }
    )
    assert response.status_code == 400
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "id": "adcc7c57-a8a7-4ed8-a5ce-d710f183b05f",
                    "name": "Машина.",
                    "type": "OFFER",
                    "price": 20000000
                }
            ],
            "updateDate": "2022-06-30T21:15:00.000Z"
        }
    )
    assert response.status_code == 200
    response = requests.get(
        sales_endpoint,
        params={"date": "2022-06-31T07:15:00.000Z"}
    )
    assert response.status_code == 400
    response = requests.get(
        sales_endpoint,
        params={"date": "2022-07-01T07:15:00.000Z"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "7e72d177-7730-4b0d-9cba-499c515715ad",
                "name": "Машина%:?*()",
                "parentId": None,
                "type": "OFFER",
                "price": 1000000,
                "date": "2022-06-30T07:15:00.000Z"
            },
            {
                "id": "adcc7c57-a8a7-4ed8-a5ce-d710f183b05f",
                "name": "Машина.",
                "parentId": None,
                "type": "OFFER",
                "price": 20000000,
                "date": "2022-06-30T21:15:00.000Z"
            }
        ]
    }
    response = requests.get(
        sales_endpoint,
        params={"date": "2022-07-01T21:15:00.000Z"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "adcc7c57-a8a7-4ed8-a5ce-d710f183b05f",
                "name": "Машина.",
                "parentId": None,
                "type": "OFFER",
                "price": 20000000,
                "date": "2022-06-30T21:15:00.000Z"
            }
        ]
    }
    response = requests.get(
        sales_endpoint,
        params={"date": "2022-07-01T21:16:00.000Z"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": []
    }
    response = requests.delete(
        delete_endpoint + "adcc7c57-a8a7-4ed8-a5ce-d710f183b05f"
    )
    assert response.status_code == 200
    response = requests.delete(
        delete_endpoint + "7e72d177-7730-4b0d-9cba-499c515715ad"
    )
    assert response.status_code == 200
