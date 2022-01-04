from pymongo import MongoClient
client = MongoClient()
twitter_db = client.twitter_database
collection = twitter_db.test

for tweet in collection.find():
    if 'public_metrics' in tweet:
        if tweet['public_metrics']['like_count'] > 10:
            print(tweet)