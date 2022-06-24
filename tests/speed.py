from datetime import datetime

import requests

start = datetime.now()
for _ in range(1000):
    requests.post('http://127.0.0.1:8000/imports',
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
print(datetime.now() - start)
