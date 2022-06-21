test_average_price = {
    "id": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
    "type": "CATEGORY",
    "name": "First",
    "parentId": None,
    "price": 672,
    "date": "2022-01-05T12:00:00.000Z",
    "children": [
        {
            "id": "7443a5a2-f31d-4dab-94c0-a7857ed6437f",
            "type": "OFFER",
            "name": "Teapot 1",
            "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
            "price": 1200,
            "date": "2022-01-05T12:00:00.000Z",
            "children": None
        },
        {
            "id": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
            "type": "CATEGORY",
            "name": "SECOND 1",
            "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
            "price": 600,
            "date": "2022-01-05T12:00:00.000Z",
            "children": [
                {
                    "id": "c0cd0e5c-89ee-4db3-9b40-1045abd42182",
                    "type": "OFFER",
                    "name": "Teapot 2 1",
                    "parentId": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
                    "price": 600,
                    "date": "2022-01-05T12:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "id": "fb53fa86-dd6f-4f30-b57c-579576b78384",
            "type": "CATEGORY",
            "name": "SECOND 2",
            "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
            "price": 445,
            "date": "2022-01-05T12:00:00.000Z",
            "children": [
                {
                    "id": "cb45dfa2-f31c-4900-a109-a13dc4a8d27b",
                    "type": "OFFER",
                    "name": "Teapot 2 2",
                    "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384",
                    "price": 770,
                    "date": "2022-01-05T12:00:00.000Z",
                    "children": None
                },
                {
                    "id": "cb45dfa2-f31c-4900-a119-a13dc4a8d27b",
                    "type": "OFFER",
                    "name": "Teapot 2 3",
                    "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384",
                    "price": 120,
                    "date": "2022-01-05T12:00:00.000Z",
                    "children": None
                }
            ]
        }
    ]
}

test_average_price_after_delete_offer = {
    "id": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
    "type": "CATEGORY",
    "name": "First",
    "parentId": None,
    "price": 856,
    "date": "2022-01-05T12:00:00.000Z",
    "children": [
        {
            "id": "7443a5a2-f31d-4dab-94c0-a7857ed6437f",
            "type": "OFFER",
            "name": "Teapot 1",
            "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
            "price": 1200,
            "date": "2022-01-05T12:00:00.000Z",
            "children": None
        },
        {
            "id": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
            "type": "CATEGORY",
            "name": "SECOND 1",
            "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
            "price": 600,
            "date": "2022-01-05T12:00:00.000Z",
            "children": [
                {
                    "id": "c0cd0e5c-89ee-4db3-9b40-1045abd42182",
                    "type": "OFFER",
                    "name": "Teapot 2 1",
                    "parentId": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
                    "price": 600,
                    "date": "2022-01-05T12:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "id": "fb53fa86-dd6f-4f30-b57c-579576b78384",
            "type": "CATEGORY",
            "name": "SECOND 2",
            "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
            "price": 770,
            "date": "2022-01-05T12:00:00.000Z",
            "children": [
                {
                    "id": "cb45dfa2-f31c-4900-a109-a13dc4a8d27b",
                    "type": "OFFER",
                    "name": "Teapot 2 2",
                    "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384",
                    "price": 770,
                    "date": "2022-01-05T12:00:00.000Z",
                    "children": None
                }
            ]
        }
    ]
}

test_average_price_and_date_after_replace_category = {
  "id": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
  "type": "CATEGORY",
  "name": "First",
  "parentId": None,
  "price": 856,
  "date": "2022-06-21T01:41:40.716Z",
  "children": [
    {
      "id": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
      "type": "CATEGORY",
      "name": "SECOND 1",
      "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
      "price": 685,
      "date": "2022-06-21T01:41:40.716Z",
      "children": [
        {
          "id": "fb53fa86-dd6f-4f30-b57c-579576b78384",
          "type": "CATEGORY",
          "name": "SECOND 2",
          "parentId": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
          "price": 685,
          "date": "2022-06-21T01:41:40.716Z",
          "children": [
            {
              "id": "c0cd0e5c-89ee-4db3-9b40-1045abd42182",
              "type": "OFFER",
              "name": "Teapot 2 1",
              "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384",
              "price": 600,
              "date": "2022-06-21T01:41:40.716Z",
              "children": None
            },
            {
              "id": "cb45dfa2-f31c-4900-a109-a13dc4a8d27b",
              "type": "OFFER",
              "name": "Teapot 2 2",
              "parentId": "fb53fa86-dd6f-4f30-b57c-579576b78384",
              "price": 770,
              "date": "2022-01-05T12:00:00.000Z",
              "children": None
            }
          ]
        }
      ]
    },
    {
      "id": "7443a5a2-f31d-4dab-94c0-a7857ed6437f",
      "type": "OFFER",
      "name": "Teapot 1",
      "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
      "price": 1200,
      "date": "2022-01-05T12:00:00.000Z",
      "children": None
    }
  ]
}

test_delete_and_update_offer_price = {
  "id": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
  "type": "CATEGORY",
  "name": "First",
  "parentId": None,
  "price": 0,
  "date": "2022-06-21T01:56:40.716Z",
  "children": [
    {
      "id": "7443a5a2-f31d-4dab-94c0-a7857ed6437f",
      "type": "OFFER",
      "name": "Teapot 1",
      "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
      "price": 0,
      "date": "2022-06-21T01:56:40.716Z",
      "children": None
    },
    {
      "id": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
      "type": "CATEGORY",
      "name": "SECOND 1",
      "parentId": "19a0a478-6a57-4f44-a2fe-0c21fb1746e9",
      "price": None,
      "date": "2022-06-21T01:41:40.716Z",
      "children": [
        {
          "id": "fb53fa86-dd6f-4f30-b57c-579576b78384",
          "type": "CATEGORY",
          "name": "SECOND 2",
          "parentId": "18df93bd-86c4-4c90-913b-0c0f897b6df6",
          "price": None,
          "date": "2022-06-21T01:41:40.716Z",
          "children": []
        }
      ]
    }
  ]
}
