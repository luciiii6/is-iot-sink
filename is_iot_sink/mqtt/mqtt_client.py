import queue
import os
import paho.mqtt.client as mqtt
from is_iot_sink.logger import LOG
from is_iot_sink.settings import Settings
from is_iot_sink.mqtt.mqtt_client_base import MQTTClientBase

class MQTTClient(MQTTClientBase):
    def __init__(self, settings: Settings):
        super().__init__(settings, settings.get("name"))
        self.__sink_id = self._settings.get('sinkId')
        self.registrationTopic = f'/{self.__sink_id}' + self._settings.get("mqtt/topics/collector/registration")
        self.dataTopic = f'/{self.__sink_id}' + self._settings.get("mqtt/topics/collector/data")
        self.valvesTopic = f'/{self.__sink_id}' + self._settings.get("mqtt/topics/valves/control")
        self.valvesStatusRequestTopic = f'/{self.__sink_id}' + self._settings.get("mqtt/topics/valves/request")
        self.irrigationModeTopic = f'/{self.__sink_id}' + self._settings.get("mqtt/topics/irrigation/mode")
        self.errorsTopic = f'/{self.__sink_id}' + self._settings.get("mqtt/topics/collector/errors")
        self._client.on_connect = self.__on_connect
        self._client.on_disconnect = self.__on_disconnect
        self._client.on_message = self.__on_message

        self.subscribe(self.registrationTopic)
        self.subscribe(self.dataTopic)
        self.subscribe(self.valvesTopic)
        self.subscribe(self.valvesStatusRequestTopic)
        self.subscribe(self.irrigationModeTopic)
        self.subscribe(self.errorsTopic)

    def attach_queue(self, queue_head: queue.Queue):
        self.__queue_head = queue_head

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to connect! Error code = {}".format(rc))
        else:
            LOG.info("MQTT Client connected successfully!")

    def __on_disconnect(self, client, userdata, rc):
        self._client.loop_stop()
        if rc != 0:
            LOG.err("MQTT Client failed to disconnect! Error code = {}".format(rc))
        else:
            LOG.info("MQTT Client disconnected successfully!")

    def __on_message(self, client, userdata, message):
        self.__queue_head.put(message)
