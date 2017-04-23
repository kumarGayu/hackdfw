from datetime import datetime
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
        [src, dest, date, userid] = data
        var = {}
        var['src'] = src
        var['dest'] = dest
        var['time'] = Database.get_mins(datetime.strptime(date.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').time())
        var['userid'] = userid
        return var

    def get_data(self,data):
        db = self.client.test
        collection = db.Ride
        doc = self.get_document(data)
        time_q = {}
        time_q['$lt'] = self.get_min(doc['time'])
        time_q['$gte'] = doc['time']
        doc['time'] = time_q
        doc['userid'] = {'$ne':doc['userid']}
        v = collection.find(doc, {'_id':0,'src':1,'dest':1,'userid':1,'time':1})
        var = {'res':[]}
        print doc
        for d in v:
            var['res'].append(d)
        return  var

    @staticmethod
    def get_min(v):
        return v+10
    @staticmethod
    def get_mins(d):
        d = str(d)
        return int(d.split(":")[0])*60+int(d.split(":")[1])

    def close(self):
        self.client.close()
if __name__ == '__main__':
    d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print type(d)
    datetime_object = datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
    print type(datetime_object)
    print datetime_object.time()