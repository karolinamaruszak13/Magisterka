import mysql.connector
from get_tweets import get_tweets
import json
from table_classes import Places, Tweets, Users, PlacesCoordinates

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Kaja25802580",
  database="twitter_database"
)

mycursor = mydb.cursor()

json_response = get_tweets(500, '2020-01-01T00:00:00.000Z', '2020-01-01T23:59:59.000Z')


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

# with open('results.json', 'w') as f:
#     f.write(json.dumps(json_response))



tweet = Tweets(mycursor)
places = Places(mycursor)
users = Users(mycursor)
places_coordinates = PlacesCoordinates(mycursor)

places.insert_many(json_response)
places_coordinates.insert_many(json_response)
users.insert_many(json_response)
tweet.insert_many(json_response)

mydb.commit()




print(mycursor.rowcount, "was inserted.")