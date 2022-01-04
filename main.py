import requests, json, sys
import pprint
from pymongo import MongoClient
client = MongoClient()
twitter_db = client.twitter_database
tweets = twitter_db.tweets
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAB86SAEAAAAA39M%2FvQlPRuBSipCabRsgYOT9aMw%3DwEbz9jQYCV5gdJnUl6RjCkjGnUhwzMUuEjyGC69pY6d2nybvAD'
headers = {'Authorization' : 'Bearer ' + bearer_token}

def get_liking_users(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}/liking_users"
    response = requests.get(url, headers=headers)
    # print(response.text)
    if "data" in json.loads(response.text):
        return json.loads(response.text)["data"]
    else:
        return {}


def get_tweets(max_results):
    url = 'https://api.twitter.com/2/tweets/search/all'
    params = {'query': '(covid vaccine OR astrazeneca OR pfizer OR sputnik OR johnson&johnson OR moderna OR curevac) -is:retweet lang:en',
              'tweet.fields': 'author_id,conversation_id,created_at,in_reply_to_user_id,public_metrics,possibly_sensitive,referenced_tweets,reply_settings',
              'expansions' : 'author_id,geo.place_id',
              'place.fields' : 'contained_within,country,country_code,name,place_type',
              'user.fields' : 'description,location,pinned_tweet_id,public_metrics,verified,protected,created_at',
              'start_time': '2021-03-27T09:51:17.000Z',
              'end_time': '2021-03-27T10:00:00.000Z',
              'max_results': max_results}
    response = requests.get(url, params=params, headers=headers)
    print(response.text)
    if response.status_code == 200:
        data = json.loads(response.text)
        for element in data["data"]:
            print(get_liking_users(element["id"]))
            element["liking_user"] = get_liking_users(element["id"])
        return data
    else:
        return None

tweets.insert(get_tweets(10))


