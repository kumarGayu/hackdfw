from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient()

    def put_data(self,data):
        db = self.client.test
        collection = db.Ride
        collection.insert_one(self.get_document(data))

    @staticmethod
    def get_document(data):
        [src, dest, date, user_id] = data
        var = {}
        var['src'] = src
        var['dest'] = dest
        var['date_time'] = date
        var['user_id'] = user_id
        return var

    def get_data(self,data):
        db = self.client.test
        collection = db.Ride
        
