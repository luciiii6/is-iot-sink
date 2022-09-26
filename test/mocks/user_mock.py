import os
import json
import paho.mqtt.client as mqttclient
from is_iot_sink.settings import Settings
from is_iot_sink.irrigation.irrigation_mode import IrrigationMode

DEFAULT_USER_ID = '621d46d1b12370d59c289ffd'

class UserMock:
    def __init__(self, settings: Settings, user_id = DEFAULT_USER_ID):
        self.__settings = settings
        self.__user_id = user_id
        self.__host = os.getenv('MQTT_HOST')
        self.__port = self.__settings.get("mqtt/port")
        self.__qos = self.__settings.get("mqtt/qos")
        self.__auth = self.__settings.get("mqtt/auth")
        self.__client = mqttclient.Client()

        if self.__auth.lower() == "on":
            self.__client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

        self.__client.connect(self.__host, self.__port)
        self.__client.loop_start()

    def __connect(self):
        if not self.__client.is_connected():
            self.__client.connect(self.__host, self.__port)

    def __publish(self, topic: str, message: str):
        self.__connect()
        self.__client.publish(topic, message, self.__qos)

    def turn_on_valve(self, valve_id):
        topic = self.__settings.get('mqtt/topics/valves/control')
        message = self.__valve_action_message(valve_id, 'TURN_ON')
        self.__publish(topic, message)

    def turn_off_valve(self, valve_id):
        topic = self.__settings.get('mqtt/topics/valves/control')
        message = self.__valve_action_message(valve_id, 'TURN_OFF')
        self.__publish(topic, message)

    def set_irrigation_mode(self, mode: IrrigationMode):
        topic = self.__settings.get('mqtt/topics/irrigation/mode')
        message = json.dumps({ "mode": IrrigationMode.mode_to_str(mode) })
        self.__publish(topic, message)

    def __valve_action_message(self, valve_id, action):
        return json.dumps(
            { 
                "valveId": valve_id,
                "action": action,
                "userId": self.__user_id
            })
