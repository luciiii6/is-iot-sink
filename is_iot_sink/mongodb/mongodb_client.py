from bson import ObjectId
from is_iot_sink.logger import LOG
from is_iot_sink.settings import Settings
import pymongo
import os
import time
import datetime

class MongoClient:
    def __init__(self, settings: Settings):
        self.__settings = settings
        self.client = pymongo.MongoClient(os.getenv('MONGODB_CONNECTION_STR'))
        self.db = self.client[self.__settings.get("mongo/db")]

    def insert_one(self, doc, collection: str):
        col = self.db[collection]
        result = col.insert_one(doc)
        return result.inserted_id

    def update_finished_irrigation(self, id):
        col = self.db[self.__settings.get("mongo/collections/irrigations")]
        result = col.update_one({'_id': ObjectId(id)}, {'$set': {'completed': True}})

    def admin_user_id(self):
        col = self.db[self.__settings.get("mongo/collections/users")]
        user = col.find_one({'UserName': 'admin'})
        return user['_id']

    def read_last_readings(self, collector_ids):
        col = self.db[self.__settings.get("mongo/collections/readings")]

        last_readings = []
        for id in collector_ids:
            pipeline = [
                {
                    '$match': {
                        'collectorId': id,
                        'soilMoisture': {
                            '$exists': 1
                        },
                        'airHumidity': {
                            '$exists': 1
                        },
                        'airTemperature': {
                            '$exists': 1
                        }
                        ,
                        'lightIntensity': {
                            '$exists': 1
                        }
                    }
                }, {
                    '$sort': {
                        'timestamp': -1
                    }
                }, {
                    '$limit': int(self.__settings.get("irrigation/automated/last_readings_count"))
                }
            ]
            readings = col.aggregate(pipeline)
            for reading in readings:
                last_readings.append(reading)

        return last_readings

    def get_users_id_for_sink(self, sink_id: str):
        col = self.db[self.__settings.get("mongo/collections/sinks")]
        sink = col.find_one({'sinkId': sink_id})
        users = sink['users']
        return users
    
    def get_user_email(self, user_id: str):
        col = self.db[self.__settings.get("mongo/collections/users")]
        user = col.find_one({'_id': ObjectId(user_id)})
        return user['Email']

    def read_first_appointment(self):
        col = self.db[self.__settings.get("mongo/collections/schedules")]

        now = datetime.datetime.now()
        in_24h = datetime.datetime.now() + datetime.timedelta(hours=24)

        pipeline = [
                      {
                        '$match': {
                          'timestamp': {
                            '$lt': in_24h.timestamp(),
                            '$gte': now.timestamp()
                          }
                        }
                      },
                      {
                        '$sort': {
                          'timestamp': -1
                        }
                      }
                    ]
        try:
            return col.aggregate(pipeline).next()
        except StopIteration:
            return None

    def cleanup(self):
        for collection in self.__settings.get("mongo/collections").values():
            self.db[collection].delete_many({})

    def __del__(self):
        self.client.close()
