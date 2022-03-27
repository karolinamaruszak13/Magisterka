import mysql.connector

#establishing the connection
conn = mysql.connector.connect(user='root', password='kaja', host='127.0.0.1')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping database MYDATABASE if already exists.
cursor.execute("DROP database IF EXISTS tweets_database")

#Preparing query to create a database
sql = "CREATE database tweets_database"

#Creating a database
cursor.execute(sql)

#Retrieving the list of databases
print("List of databases: ")
cursor.execute("SHOW DATABASES")
print(cursor.fetchall())

#Closing the connection
conn.close()