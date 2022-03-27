import mysql.connector
from table_classes import Places, Tweets, Users, PlacesCoordinates

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Kaja25802580",
  database="twitter_database"
)

mycursor = mydb.cursor()


tweet = Tweets(mycursor)
places = Places(mycursor)
users = Users(mycursor)
places_coordinates = PlacesCoordinates(mycursor)

places_coordinates.delete_rows()
tweet.delete_rows()
places.delete_rows()
users.delete_rows()

mydb.commit()

print(mycursor.rowcount, "record(s) deleted")