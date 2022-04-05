import requests, json, sys
from os import stat
from datetime import datetime, timedelta
import json

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAB86SAEAAAAA39M%2FvQlPRuBSipCabRsgYOT9aMw%3DwEbz9jQYCV5gdJnUl6RjCkjGnUhwzMUuEjyGC69pY6d2nybvAD'
headers = {'Authorization' : 'Bearer ' + bearer_token}

def get_liking_users(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}/liking_users"
    response = requests.get(url, headers=headers)
    # print(response.text)
    if "data" in json.loads(response.text):
        return json.loads(response.text)["data"]
    else:
        return []

def get_tweets(max_results, start_time, end_time):
    url = 'https://api.twitter.com/2/tweets/search/all'
    params = {'query': '(covid vaccine OR astrazeneca OR pfizer OR sputnik OR johnson&johnson OR moderna OR curevac) -is:retweet lang:en',
              'tweet.fields': 'id,author_id,conversation_id,text,created_at,geo,in_reply_to_user_id,public_metrics,possibly_sensitive,referenced_tweets',
              'expansions' : 'author_id,geo.place_id,referenced_tweets.id',
              'place.fields' : 'full_name,id,country,country_code,geo,name,place_type',
              'user.fields' : 'id,name,username,description,location,pinned_tweet_id,public_metrics,verified,created_at,profile_image_url,url',
              'start_time': start_time,
              'end_time': end_time,
              'max_results': max_results}
    response = requests.get(url, params=params, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        data = json.loads(response.text)
        for element in data["data"]:
            users_liked = {"users_liked": get_liking_users(element["id"])}
            element.update(users_liked)
        return data
    else:
        return None


# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)

# start_time = datetime(2020, 1, 1, 0, 0, 0)
# end_time = datetime(2020, 1, 1, 23, 59, 59)
# delta = timedelta(days=1)

# for single_date in daterange(start_time, end_time + delta):
#     print(single_date)
#     get_tweets(10, single_date.isoformat() + '.000Z',  (single_date + delta).isoformat() + '.000Z')
    # print(single_date.isoformat() + '.000Z')


# json_resposne = get_tweets(500, '2020-01-01T00:00:00.000Z', '2020-01-02T00:00:00.000Z')

# with open('results.json', 'w') as f:
#     f.write(json.dumps(json_resposne))

