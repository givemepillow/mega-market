import requests

DATA = {
    "items": [
        {
            "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
            "name": "Самая главная категория",
            "type": "CATEGORY"
        },
        {
            "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
            "name": "Овощи",
            "type": "CATEGORY"
        },
        {
            "id": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "name": "Фрукты",
            "type": "CATEGORY"
        },
        {
            "id": "b4c19438-40cb-497e-9f32-fcf4a92b3990",
            "name": "Персики",
            "type": "OFFER",
            "price": 100
        },
        {
            "id": "4b2902ab-cd80-428a-881b-2c3e1953b6e5",
            "name": "Ананасы",
            "type": "OFFER",
            "price": 200
        },
        {
            "id": "e30a3fbc-d013-4b57-8220-295a388afe98",
            "name": "Груши",
            "type": "OFFER",
            "price": 120
        },
        {
            "id": "d8aad5d9-8524-46f0-8941-85ad9289114d",
            "name": "Помидорка",
            "type": "OFFER",
            "price": 190
        },
        {
            "id": "3c21557c-6758-4869-a961-102245062fd6",
            "name": "Картошечка",
            "type": "OFFER",
            "price": 135
        },
        {
            "id": "127e8b34-c684-4aea-8b89-00b37d1cf88c",
            "name": "Огурчик",
            "type": "OFFER",
            "price": 165
        }
    ],
    "updateDate": "2022-07-07T15:00:00.000Z"
}


def test_statistic_for_offer_and_category(imports_endpoint, statistic_endpoint):
    response = requests.post(imports_endpoint, json=DATA)
    assert response.status_code == 200
    response = requests.get(statistic_endpoint("9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a"))
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-07-07T15:00:00.000Z"
            }
        ]
    }
    response = requests.get(
        statistic_endpoint("4b2902ab-cd80-428a-881b-2c3e1953b6e5"),
        params={"dateStart": "2022-07-07T15:00:01.000Z"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": []
    }


DATA2 = {
    "items": [
        {
            "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
            "name": "Овощи",
            "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
            "type": "CATEGORY"
        },
        {
            "id": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "name": "Фрукты",
            "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
            "type": "CATEGORY"
        },
        {
            "id": "b4c19438-40cb-497e-9f32-fcf4a92b3990",
            "name": "Персики",
            "parentId": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "type": "OFFER",
            "price": 100
        },
        {
            "id": "4b2902ab-cd80-428a-881b-2c3e1953b6e5",
            "name": "Ананасы",
            "parentId": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "type": "OFFER",
            "price": 200
        },
        {
            "id": "e30a3fbc-d013-4b57-8220-295a388afe98",
            "name": "Груши",
            "parentId": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "type": "OFFER",
            "price": 120
        },
        {
            "id": "d8aad5d9-8524-46f0-8941-85ad9289114d",
            "name": "Помидорка",
            "parentId": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
            "type": "OFFER",
            "price": 190
        },
        {
            "id": "3c21557c-6758-4869-a961-102245062fd6",
            "name": "Картошечка",
            "parentId": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
            "type": "OFFER",
            "price": 135
        },
        {
            "id": "127e8b34-c684-4aea-8b89-00b37d1cf88c",
            "parentId": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
            "name": "Огурчик",
            "type": "OFFER",
            "price": 165
        }
    ],
    "updateDate": "2022-07-31T23:59:00.000Z"
}


def test_statistic_after_add_to_tree(imports_endpoint, statistic_endpoint):
    response = requests.post(imports_endpoint, json=DATA2)
    assert response.status_code == 200
    response = requests.get(statistic_endpoint("73c4c066-e21d-45b6-8e21-ef575a389b0d"))
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": 163,
                "date": "2022-07-31T23:59:00.000Z"
            },
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-07-07T15:00:00.000Z"
            }
        ]
    }
    response = requests.get(
        statistic_endpoint("3c21557c-6758-4869-a961-102245062fd6"),
        params={"dateStart": "2022-07-20T15:15:00.000Z"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "3c21557c-6758-4869-a961-102245062fd6",
                "name": "Картошечка",
                "parentId": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "type": "OFFER",
                "price": 135,
                "date": "2022-07-31T23:59:00.000Z"
            }
        ]
    }
    response = requests.get(
        statistic_endpoint("9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a"),
        params={
            "dateStart": "2022-07-08T15:00:00.000Z",
            "dateEnd": "2022-07-31T23:59:00.000Z"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": 151,
                "date": "2022-07-31T23:59:00.000Z"
            }
        ]
    }


DATA3 = {
    "items": [
        {
            "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
            "name": "Овощи",
            "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
            "type": "CATEGORY"
        },
        {
            "id": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "name": "Фрукты",
            "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
            "type": "CATEGORY"
        },
        {
            "id": "b4c19438-40cb-497e-9f32-fcf4a92b3990",
            "name": "Персики",
            "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
            "type": "OFFER",
            "price": 100
        },
        {
            "id": "4b2902ab-cd80-428a-881b-2c3e1953b6e5",
            "name": "Ананасы",
            "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
            "type": "OFFER",
            "price": 200
        },
        {
            "id": "d8aad5d9-8524-46f0-8941-85ad9289114d",
            "name": "Помидорка",
            "parentId": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "type": "OFFER",
            "price": 190
        },
        {
            "id": "3c21557c-6758-4869-a961-102245062fd6",
            "name": "Картошечка",
            "parentId": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
            "type": "OFFER",
            "price": 135
        },
        {
            "id": "127e8b34-c684-4aea-8b89-00b37d1cf88c",
            "parentId": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
            "name": "Огурчик",
            "type": "OFFER",
            "price": 165
        }
    ],
    "updateDate": "2022-08-08T08:08:08.000Z"
}


def test_statistic_after_replace(imports_endpoint, statistic_endpoint):
    response = requests.post(imports_endpoint, json=DATA3)
    assert response.status_code == 200
    response = requests.get(statistic_endpoint("9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a"))
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": 151,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": 151,
                "date": "2022-07-31T23:59:00.000Z"
            },
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-07-07T15:00:00.000Z"
            }
        ]
    }
    response = requests.get(statistic_endpoint("73c4c066-e21d-45b6-8e21-ef575a389b0d"))
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": 135,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": 163,
                "date": "2022-07-31T23:59:00.000Z"
            },
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-07-07T15:00:00.000Z"
            }
        ]
    }
    response = requests.get(statistic_endpoint("cd9cfe40-890c-4547-b2b2-3f9e817c14a8"))
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
                "name": "Фрукты",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": 158,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
                "name": "Фрукты",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": 140,
                "date": "2022-07-31T23:59:00.000Z"
            },
            {
                "id": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
                "name": "Фрукты",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-07-07T15:00:00.000Z"
            }
        ]
    }
    response = requests.get(statistic_endpoint("e30a3fbc-d013-4b57-8220-295a388afe98"))
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "e30a3fbc-d013-4b57-8220-295a388afe98",
                "name": "Груши",
                "parentId": "cd9cfe40-890c-4547-b2b2-3f9e817c14a8",
                "type": "OFFER",
                "price": 120,
                "date": "2022-07-31T23:59:00.000Z"
            },
            {
                "id": "e30a3fbc-d013-4b57-8220-295a388afe98",
                "name": "Груши",
                "parentId": None,
                "type": "OFFER",
                "price": 120,
                "date": "2022-07-07T15:00:00.000Z"
            }
        ]
    }


def test_statistic_after_deletion(delete_endpoint, statistic_endpoint, sort):
    response = requests.delete(delete_endpoint + "3c21557c-6758-4869-a961-102245062fd6")
    assert response.status_code == 200
    response = requests.get(statistic_endpoint("73c4c066-e21d-45b6-8e21-ef575a389b0d"))
    assert response.json() == {
        "items": [
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": 135,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": None,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "type": "CATEGORY",
                "price": 163,
                "date": "2022-07-31T23:59:00.000Z"
            },
            {
                "id": "73c4c066-e21d-45b6-8e21-ef575a389b0d",
                "name": "Овощи",
                "parentId": None,
                "type": "CATEGORY",
                "price": None,
                "date": "2022-07-07T15:00:00.000Z"
            }
        ]
    }
    response = requests.get(statistic_endpoint("3c21557c-6758-4869-a961-102245062fd6"))
    assert response.status_code == 404
    response = requests.delete(delete_endpoint + "4b2902ab-cd80-428a-881b-2c3e1953b6e5")
    assert response.status_code == 200
    response = requests.delete(delete_endpoint + "cd9cfe40-890c-4547-b2b2-3f9e817c14a8")
    assert response.status_code == 200
    response = requests.get(
        statistic_endpoint("9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a"),
        params={
            "dateStart": "2022-08-08T08:08:08.000Z",
            "dateEnd": "2022-08-08T08:08:08.000Z"
        }
    )
    assert response.json() == {
        "items": [
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": 151,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": 155,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": 143,
                "date": "2022-08-08T08:08:08.000Z"
            },
            {
                "id": "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a",
                "name": "Самая главная категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": 100,
                "date": "2022-08-08T08:08:08.000Z"
            }
        ]
    }
    response = requests.delete(delete_endpoint + "9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a")
    assert response.status_code == 200
    response = requests.get(statistic_endpoint("9e672ebf-d9e9-4e9f-ba64-cbad77ee9a2a"))
    assert response.status_code == 404
