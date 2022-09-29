import os
import json
from is_iot_sink.mongodb.mongodb_client import MongoClient
import paho.mqtt.client as mqttclient
from is_iot_sink.settings import Settings
from is_iot_sink.irrigation.irrigation_mode import IrrigationMode
from is_iot_sink.mqtt.mqtt_client_base import MQTTClientBase

DEFAULT_USER_ID = '621d46d1b12370d59c289ffd'

class UserMock(MQTTClientBase):
    def __init__(self, settings: Settings, mongo_client: MongoClient, user_id = DEFAULT_USER_ID):
        super().__init__(settings, "user" + user_id)
        self.__user_id = user_id
        self.__mongo_client = mongo_client

    def turn_on_valve(self, valve_id):
        topic = self._settings.get('mqtt/topics/valves/control')
        message = self.__valve_action_message(valve_id, 'TURN_ON')
        self.publish(topic, message)

    def turn_off_valve(self, valve_id):
        topic = self._settings.get('mqtt/topics/valves/control')
        message = self.__valve_action_message(valve_id, 'TURN_OFF')
        self.publish(topic, message)

    def set_irrigation_mode(self, mode: IrrigationMode):
        topic = self._settings.get('mqtt/topics/irrigation/mode')
        message = json.dumps({ "mode": IrrigationMode.mode_to_str(mode) })
        self.publish(topic, message)

    def create_schedule(self, timestamp, duration):
        document = self.__create_schedule_document_nodump(timestamp, duration)
        self.__mongo_client.insert_one(document, self._settings.get("mongo/collections/schedules"))

    def __valve_action_message(self, valve_id, action):
        return json.dumps(
            {
                "valveId": valve_id,
                "action": action,
                "userId": self.__user_id
            })

    def __create_schedule_document(self, timestamp, duration):
        return json.dumps(
            {
                "timestamp": timestamp,
                "duration": duration
            })

    def __create_schedule_document_nodump(self, timestamp, duration):
        return {
                "timestamp": timestamp,
                "duration": duration
               }
