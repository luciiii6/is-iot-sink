import os
import json
import paho.mqtt.client as mqttclient
from is_iot_sink.settings import Settings
from is_iot_sink.mqtt.mqtt_client_base import MQTTClientBase

class CollectorMock(MQTTClientBase):
    def __init__(self, id, settings: Settings):
        super().__init__(settings, "collector" + id)
        self.__id = id

    def register(self, topic):
        register_message = json.dumps({'collectorId' : self.__id})
        self.publish(topic, register_message)

    def send_dummy_data(self, topic):
        self.publish(topic, self.__dummy_data())

    def __dummy_data(self):
        return json.dumps(
            {
                "collectorId": self.__id,
                "soilMoisture": [
                    50,
                    50
                ],
                "timestamp": 1696969420,
                "airTemperature": 10,
                "airHumidity": 50,
                "lightIntensity": 50
            })
