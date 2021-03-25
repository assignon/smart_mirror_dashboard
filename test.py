import requests

BASE = 'http://localhost:5000/'

response = requests.put(BASE + 'user/1', json={'login':'SebasC96'})
print(response.json())
input()

response = requests.get(BASE + 'users')
print(response.json())