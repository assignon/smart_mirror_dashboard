import requests

BASE = 'http://localhost:5000/'

response = requests.post(BASE + 'users', json={'name':'test','login':'         ', 'password':'password123', 'is_admin':True})
print(response.json())
input()

response = requests.get(BASE + 'users')
print(response.json())