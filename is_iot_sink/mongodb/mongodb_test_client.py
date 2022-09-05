from is_iot_sink.mongodb.mongodb_client import MongoClient

class MongoTestClient(MongoClient):
    def __init__(self):
        MongoClient.__init__(self)

    def clean_up(self):
        for collection in self.collections:
            self.db[collection].delete_many({})
