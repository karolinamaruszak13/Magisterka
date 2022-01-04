import requests, json, sys
import pprint
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAB86SAEAAAAA39M%2FvQlPRuBSipCabRsgYOT9aMw%3DwEbz9jQYCV5gdJnUl6RjCkjGnUhwzMUuEjyGC69pY6d2nybvAD'

url = 'https://api.twitter.com/2/tweets/1243477619812765697/liking_users'
headers = {'Authorization' : 'Bearer ' + bearer_token}
params = None
response = requests.get(url, params=params, headers=headers)
data = []
if response.status_code == 200:
    data = json.loads(response.text)


print(response.text)

