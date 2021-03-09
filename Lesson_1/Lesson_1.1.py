import requests
import json


url = 'https://api.github.com'
user='masterjr86'

r = requests.get(f'{url}/users/{user}/repos')


for i in r.json():
    print(i['name'])


with open('data.json', 'w') as f:
    json.dump(r.json(), f)






