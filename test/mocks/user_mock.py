import os
import json
import paho.mqtt.client as mqttclient
from is_iot_sink.settings import Settings
from is_iot_sink.irrigation.irrigation_mode import IrrigationMode
from is_iot_sink.mqtt.mqtt_client_base import MQTTClientBase

DEFAULT_USER_ID = '621d46d1b12370d59c289ffd'

class UserMock(MQTTClientBase):
    def __init__(self, settings: Settings, user_id = DEFAULT_USER_ID):
        super().__init__(settings, "user" + user_id)
        self.__user_id = user_id

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

    def __valve_action_message(self, valve_id, action):
        return json.dumps(
            { 
                "valveId": valve_id,
                "action": action,
                "userId": self.__user_id
            })
