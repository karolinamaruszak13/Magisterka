import mysql.connector
from get_tweets import get_tweets
import json
from table_classes import Places, Tweets, Users, PlacesCoordinates, UsersLiked
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Kaja25802580",
  database="twitter_database"
)

mycursor = mydb.cursor()

# start_date = '2020-03-12T12:00:00.000Z'
# end_date = '2020-03-12T13:00:00.000Z'
for j in range(23, 31):
  for i in range(10, 23):
    if i >= 10:
      start_date = f"2021-11-{j}T{i}:00:00.000Z"
      end_date = f"2021-11-{j}T{i+1}:00:00.000Z"
      print(start_date, end_date)
    elif i == 9:
      start_date = f"2021-11-{j}T0{i}:00:00.000Z"
      end_date = f"2021-11-{j}T{i+1}:00:00.000Z"
      print(start_date, end_date)
    else:
      start_date = f"2021-11-{j}T0{i}:00:00.000Z"
      end_date = f"2021-11-{j}T0{i+1}:00:00.000Z"
      print(start_date, end_date)


    json_response = get_tweets(300, start_date, end_date)
    with open(f'results_{start_date[:11]}.json', 'w+') as f:
      f.write(json.dumps(json_response))

    # with open(f'results_{start_date[:11]}.json', 'r') as f:
    #   json_response = json.loads(f.read())
    # print(json_response['data'][0])

    tweet = Tweets(mycursor)
    places = Places(mycursor)
    users = Users(mycursor)
    places_coordinates = PlacesCoordinates(mycursor)
    users_liked = UsersLiked(mycursor)

    places.insert_many(json_response)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

    places_coordinates.insert_many(json_response)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

    users.insert_many(json_response['includes'].get('users', []))
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

    tweet.insert_many(json_response, mydb)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")





    df_users =  pd.read_sql("select id from users", mydb)
    u = users_liked.get_data(json_response)
    users_to_add = []
    from get_users_liked import get_users
    for _, user in u:
      if user not in df_users['id'].values:
        users_to_add.append(user)

    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    for chunk in chunks(users_to_add, 100):
      chunk_users = ",".join(chunk)
      users.insert_many(get_users(chunk_users))
      # print(get_users(chunk_users))
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

    users_liked.insert_many(json_response)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")