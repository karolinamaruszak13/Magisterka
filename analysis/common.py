import mysql.connector
import csv

vaccines_dict = {
    'astrazeneca' : {
        'display_name' : 'Astrazeneca',
        'color' : 'b'
    },
    'pfizer' : {
        'display_name' : 'Pfizer',
        'color' : 'g'
    },
    'sputnik' : {
        'display_name' : 'Sputnik V',
        'color' : 'r'
    },
    'moderna' : {
        'display_name' : 'Moderna',
        'color' : 'c'
    },
    'curevac' : {
        'display_name' : 'CureVac',
        'color' : 'm'
    },
    'johnson &amp; johnson' : {
        'display_name' : 'Johnson & Johnson',
        'color' : 'y'
    }
}

mydb = None

def getDbConn():
    global mydb
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kaja25802580",
    database="twitter_database"
    )
    return mydb

def getDbCursor():
    if mydb == None:
        getDbConn()
    return mydb.cursor()

def getCountryNames():
    country_names = {}
    with open('country_codes.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            country_names[row[1]] = row[0]
    return country_names