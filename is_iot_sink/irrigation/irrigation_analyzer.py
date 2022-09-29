from is_iot_sink.logger import LOG
from is_iot_sink.settings import Settings
from is_iot_sink.notifier.mailer import Mailer
from is_iot_sink.mongodb.mongodb_client import MongoClient


class IrrigationAnalyzer:
    def __init__(self, mongo_client: MongoClient, settings: Settings) -> None:
        self.__mongo_client = mongo_client
        self.__mailer = Mailer()
        self.__settings = settings
        self.__sinkId = self.__get_sink_id()
        self.__collector_ids = self.__get_colector_ids(self.__sinkId)
        self.__first_values = self.__get_values(self.__collector_ids)
        self.__last_values = None
    
    def __get_values(self, collector_ids: list):
        readings = self.__mongo_client.read_last_readings(collector_ids, 1)
        relevant_values = []
        for reading in readings:
            intermediary = {}
            intermediary['collectorId'] = reading['collectorId']
            intermediary['airHumidity'] = reading['airHumidity']
            intermediary['soilMoisture'] = reading['soilMoisture']
            relevant_values.append(intermediary)
        
        return relevant_values

    def set_last_values(self):
        self.__last_values = self.__get_values(self.__collector_ids)

    def perform_analisys(self):
        self.set_last_values()
        sorted_first = sorted(self.__first_values, key=lambda k:k['collectorId'])
        sorted_last = sorted(self.__last_values, key=lambda k:k['collectorId'])
        errors = ''
        for i in range(len(sorted_first)):
            if sorted_first[i]['airHumidity'] >= sorted_last[i]['airHumidity']:
                errors += f"Air Humidity did not increase after irrigation for colector {sorted_first[i]['collectorId']}\n"
            if sorted_first[i]['soilMoisture'] >= sorted_last[i]['soilMoisture']:
                errors += f"Soil moisture did not increase after irrigation for colector {sorted_first[i]['collectorId']}\n"
        
        if errors:
            users = self.__mongo_client.get_users_id_for_sink(self.__settings.get('sinkId'))
            emails = [self.__mongo_client.get_user_email(user) for user in users]
            self.__mailer.send_mail_for_sink_errors(emails, errors)

    def __get_colector_ids(self, sink_id: str) -> list:
        collectors = self.__mongo_client.get_collectors_for_sink(sink_id)
        return collectors
    
    def __get_sink_id(self) -> str:
        return self.__settings.get('sinkId')
