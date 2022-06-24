import requests

with open('res.json', 'r', encoding='utf-8') as f:
    r = requests.post('http://127.0.0.1:8000/imports', data=f.read())
    print(r.status_code)
