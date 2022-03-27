from abc import abstractmethod
import datetime



class Table:
    def __init__(self, cursor):
        self.cursor = cursor

    @property
    @abstractmethod
    def sql_insert(self):
        pass

    @property
    @abstractmethod
    def sql_delete(self):
        pass

    
    @abstractmethod
    def get_data(self):
        pass


    @abstractmethod
    def insert_many(self):
        pass

    @abstractmethod
    def delete_rows(self):
        pass


class Tweets(Table):
    def __init__(self, cursor):
        super().__init__(cursor)

    @property
    def sql_insert(self):
        return "INSERT INTO tweets (\
                id,\
                author_id,\
                place_id,\
                tweet_text,\
                retweet_count,\
                reply_count,\
                like_count,\
                created_at,\
                possibly_sensitive,\
                conversation_id,\
                in_reply_to_userid,\
                quote_count)\
                VALUES(%s,%s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s)"
    
    @property
    def sql_delete(self):
        return "DELETE FROM tweets"

   
    def get_data(self, response: dict) -> list:
        final_data = []
        for tweet in response['data']:
            values = []
            values.append(tweet["id"])
            values.append(tweet["author_id"])
            if "geo" in tweet:
                values.append(tweet["geo"]["place_id"])               
            else:
                values.append(None)
            values.append(tweet["text"])
            values.append(tweet["public_metrics"]["retweet_count"])
            values.append(tweet["public_metrics"]["reply_count"])
            values.append(tweet["public_metrics"]["like_count"])
            values.append(datetime.datetime.strptime(tweet['created_at'],'%Y-%m-%dT%H:%M:%S.%f%z'))
            values.append(tweet["possibly_sensitive"])
            values.append(tweet.get("conversation_id", None))
            values.append(tweet.get("in_reply_to_user_id", None))
            values.append(tweet["public_metrics"]["quote_count"])
            final_data.append(values)
        return final_data

   
    def insert_many(self, json_response):
        return self.cursor.executemany(self.sql_insert, self.get_data(json_response))

    def delete_rows(self):
        return self.cursor.execute(self.sql_delete)  

class Places:
    def __init__(self, cursor):
        self.cursor = cursor

    @property
    def sql_insert(self):
        return  "INSERT INTO places (\
                id,\
                full_name,\
                country,\
                country_code,\
                name,\
                place_type)\
                VALUES(%s,%s,\
                %s,\
                %s,\
                %s,\
                %s)"
    
    @property
    def sql_delete(self):
        return "DELETE FROM places"

   
    def get_data(self, response: dict) -> list:
        places = []
        for place in response['includes'].get('places', []):
            place_columns = []
            place_columns.append(place["id"])
            place_columns.append(place.get("full_name", None))
            place_columns.append(place.get("country", None))
            place_columns.append(place.get("country_code", None))
            place_columns.append(place.get("name"))
            place_columns.append(place.get("place_type", None))
            places.append(place_columns)
        return places

        
   
    def insert_many(self, json_response):
        return self.cursor.executemany(self.sql_insert, self.get_data(json_response))

    def delete_rows(self):
        return self.cursor.execute(self.sql_delete) 


class Users:
    def __init__(self, cursor):
        self.cursor = cursor

    @property
    def sql_insert(self):
        return  "INSERT INTO users (\
                id,\
                name,\
                username,\
                description,\
                location,\
                pinned_tweet_id,\
                created_at,\
                profile_image_url,\
                url,\
                followers_count,\
                following_count,\
                tweet_count,\
                listed_count)\
                VALUES(%s,%s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s)"
    
    @property
    def sql_delete(self):
        return "DELETE FROM users"

   
    def get_data(self, response: dict) -> list:
        users = []
        for user in response['includes'].get('users', []):
            users_columns = []
            users_columns.append(user["id"])
            users_columns.append(user.get("name", None))
            users_columns.append(user.get("username", None))
            users_columns.append(user.get("description", None))
            users_columns.append(user.get("location"))
            users_columns.append(user.get("pinned_tweet_id", None))
            users_columns.append(datetime.datetime.strptime(user['created_at'],'%Y-%m-%dT%H:%M:%S.%f%z'))
            users_columns.append(user.get("profile_image_url", None))
            users_columns.append(user.get("url", None))
            users_columns.append(user["public_metrics"]["followers_count"])
            users_columns.append(user["public_metrics"]["following_count"])
            users_columns.append(user["public_metrics"]["tweet_count"])
            users_columns.append(user["public_metrics"]["listed_count"])
            users.append(users_columns)
        return users

        
    def insert_many(self, json_response):
        return self.cursor.executemany(self.sql_insert, self.get_data(json_response))


    def delete_rows(self):
        return self.cursor.execute(self.sql_delete)
    

class PlacesCoordinates:
    def __init__(self, cursor):
        self.cursor = cursor

    @property
    def sql_insert(self):
        return  "INSERT INTO place_coordinates (\
                id,\
                latitude,\
                longitude)\
                VALUES(%s,%s,\
                %s)"
    
    @property
    def sql_delete(self):
        return "DELETE FROM place_coordinates"

   
    def get_data(self, response: dict) -> list:
        coordinates = []
        for coordinate in response['data']:
            coordinate_columns = []
            if "geo" and "coordinates" in coordinate:
                coordinate_columns.append(coordinate["geo"]["place_id"])
                coordinate_columns.append(coordinate["geo"]["coordinates"]["coordinates"][0])
                coordinate_columns.append(coordinate["geo"]["coordinates"]["coordinates"][1])          
            else:
                coordinate_columns.append(None)  
                coordinate_columns.append(None) 
                coordinate_columns.append(None)  
            coordinates.append(coordinate_columns)
        return coordinates

        
    def insert_many(self, json_response):
        return self.cursor.executemany(self.sql_insert , self.get_data(json_response))


    def delete_rows(self):
        return self.cursor.execute(self.sql_delete)
    
