import queue
import os
import paho.mqtt.client as mqtt
from is_iot_sink.logger import LOG
from is_iot_sink.settings import Settings

class MQTTClientBase:
    def __init__(self, settings: Settings, name = ""):
        self._settings = settings
        self._host = os.getenv('MQTT_HOST')
        self._port = int(self._settings.get("mqtt/port"))
        self._qos = int(self._settings.get("mqtt/qos"))
        self._auth = self._settings.get("mqtt/auth")
        self._client = mqtt.Client(name)

        if self._auth.lower() == "on":
            self._client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

        try:
            self._client.connect(self._host, self._port)
            self._client.loop_start()
        except Exception as ex:
            LOG.err("MQTT Client failed to start! : {}".format(ex))

    def _connect(self):
        if not self._client.is_connected():
            self._client.connect(self._host, self._port)

    def _disconnect(self):
        self._client.disconnect()

    def subscribe(self, topic: str):
        self._client.subscribe(topic, self._qos)

    def publish(self, topic: str, message: str):
        try:
            self._connect()
        except Exception:
            LOG.err("MQTT Client failed to connect!")
            return

        try:
            self._client.publish(topic, message, self._qos)
        except Exception as ex:
            LOG.err("MQTT Client failed to publish!")
