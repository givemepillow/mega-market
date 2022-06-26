import requests


def test_import_and_delete_one_item(imports_endpoint, delete_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "type": "OFFER",
                    "name": "Teapot",
                    "id": "4b31f4d1-ba85-4908-9a92-a98dec759016",
                    "price": 1999,
                    "parentId": None
                }
            ],
            "updateDate": "2022-02-10T12:00:00.000Z"
        }
    )
    assert response.status_code == 200
    response = requests.delete(
        delete_endpoint + "4b31f4d1-ba85-4908-9a92-a98dec759016"
    )
    assert response.status_code == 200
    response = requests.delete(
        delete_endpoint + "4b31f4d1-ba85-4908-9a92-a98dec759016"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }


def test_import_and_delete_items(imports_endpoint, delete_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "type": "OFFER",
                    "name": "Teapot Blue",
                    "id": "9a293f76-75d7-4258-b244-d6477f28d010",
                    "price": 3999,
                },
                {
                    "type": "CATEGORY",
                    "name": "Books",
                    "id": "da96d714-9fe8-4e75-a74f-3ba54c583853",
                },
                {
                    "type": "CATEGORY",
                    "name": "Computer Books",
                    "id": "45798ab3-7404-4f98-85bd-9640d0e7719a",
                    "parentId": "da96d714-9fe8-4e75-a74f-3ba54c583853"
                }
            ],
            "updateDate": "2022-02-21T12:00:00.000Z"
        }
    )
    assert response.status_code == 200
    response = requests.delete(
        delete_endpoint + "9a293f76-75d7-4258-b244-d6477f28d010"
    )
    assert response.status_code == 200
    response = requests.delete(
        delete_endpoint + "45798ab3-7404-4f98-85bd-9640d0e7719a"
    )
    assert response.status_code == 200
    response = requests.delete(
        delete_endpoint + "da96d714-9fe8-4e75-a74f-3ba54c583853"
    )
    assert response.status_code == 200
    # after deletion
    response = requests.delete(
        delete_endpoint + "9a293f76-75d7-4258-b244-d6477f28d010"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }
    response = requests.delete(
        delete_endpoint + "45798ab3-7404-4f98-85bd-9640d0e7719a"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }
    response = requests.delete(
        delete_endpoint + "da96d714-9fe8-4e75-a74f-3ba54c583853"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }


def test_import_and_delete_category_with_items(imports_endpoint, delete_endpoint):
    response = requests.post(
        imports_endpoint,
        json={
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Video Cards",
                    "id": "80ea8f97-fd4a-4098-bd81-8728929dd925",
                },
                {
                    "type": "CATEGORY",
                    "name": "NVIDIA",
                    "id": "0911b3fa-07bb-46a6-89fa-c4996a548939",
                    "parentId": "80ea8f97-fd4a-4098-bd81-8728929dd925",
                },
                {
                    "type": "CATEGORY",
                    "name": "AMD",
                    "id": "1502b962-4c34-4f1b-a1e9-5656e19d6065",
                    "parentId": "80ea8f97-fd4a-4098-bd81-8728929dd925",
                },
                {
                    "type": "OFFER",
                    "name": "gtx 3090",
                    "id": "37d9e437-15b8-4027-9d82-ecfe6fd2525d",
                    "parentId": "0911b3fa-07bb-46a6-89fa-c4996a548939",
                    "price": 108000
                },
                {
                    "type": "OFFER",
                    "name": "gtx 2080",
                    "id": "430a63d5-8401-4f2c-af24-e3b72db8d843",
                    "parentId": "0911b3fa-07bb-46a6-89fa-c4996a548939",
                    "price": 108000
                },
                {
                    "type": "OFFER",
                    "name": "rx 6600",
                    "id": "cc99524b-a8e9-4bf3-a4a9-ff3d4656c379",
                    "parentId": "1502b962-4c34-4f1b-a1e9-5656e19d6065",
                    "price": 90000
                }
            ],
            "updateDate": "2022-12-31T03:06:22+00:00"
        }
    )
    assert response.status_code == 200
    # Video Cards
    response = requests.delete(
        delete_endpoint + "80ea8f97-fd4a-4098-bd81-8728929dd925"
    )
    assert response.status_code == 200
    # rx 6600
    response = requests.delete(
        delete_endpoint + "cc99524b-a8e9-4bf3-a4a9-ff3d4656c379"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }
    # gtx 2080
    response = requests.delete(
        delete_endpoint + "430a63d5-8401-4f2c-af24-e3b72db8d843"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }
    # gtx 3090
    response = requests.delete(
        delete_endpoint + "37d9e437-15b8-4027-9d82-ecfe6fd2525d"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }
    # AMD
    response = requests.delete(
        delete_endpoint + "1502b962-4c34-4f1b-a1e9-5656e19d6065"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }
    # NVIDIA
    response = requests.delete(
        delete_endpoint + "0911b3fa-07bb-46a6-89fa-c4996a548939"
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "Item not found"
    }

