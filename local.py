import requests

res=requests.get("http://127.0.0.1:1000/api")
print(res.json())