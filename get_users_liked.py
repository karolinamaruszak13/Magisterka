from typing import List
import requests, json, sys


bearer_token = 'AAAAAAAAAAAAAAAAAAAAAB86SAEAAAAA39M%2FvQlPRuBSipCabRsgYOT9aMw%3DwEbz9jQYCV5gdJnUl6RjCkjGnUhwzMUuEjyGC69pY6d2nybvAD'
headers = {'Authorization' : 'Bearer ' + bearer_token}
users = '964321751030145024,247363095'

def get_users(ids: str) -> List[dict]:
    if ids.count(',') > 99:
        raise Exception('Number of users is larger than 100')        
    url = 'https://api.twitter.com/2/users'
    params = {
        'ids': ids,
        'user.fields' : 'id,name,username,description,location,pinned_tweet_id,public_metrics,verified,created_at,profile_image_url,url'
    }
    response = requests.get(url, params=params, headers=headers)
    if "data" in json.loads(response.text):
        return json.loads(response.text)["data"]
    else:
        return []

# print(get_users(users))

