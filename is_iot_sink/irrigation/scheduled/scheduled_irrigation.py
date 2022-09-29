import datetime

from is_iot_sink.irrigation.irrigation_mode import *
from is_iot_sink.irrigation.valves.valves_manager import ValveManager
from is_iot_sink.mongodb.mongodb_client import MongoClient
from is_iot_sink.settings import Settings
from is_iot_sink.logger import LOG
import time
import threading


class ScheduledIrrigation:
    def __init__(self, valve_manager: ValveManager, mongo_client: MongoClient):
        self.__valve_manager = valve_manager
        self.__mongo_client = mongo_client
        self.mode = IrrigationMode.SCHEDULED
        self.running = False
        self.global_thread = threading.Thread(target=self.__run, daemon=True)

    def start(self):
        LOG.info("Scheduled Irrigation process started.")
        self.running = True
        self.global_thread.start()

    def stop(self):
        LOG.info("Scheduled Irrigation process stopped.")
        self.running = False
        self.global_thread.join()

    def __run(self):
        appointment = None
        copy_of_appointment = None

        while self.running:
            appointment = self.__mongo_client.read_first_appointment()

            if appointment and copy_of_appointment != appointment and not self.__valve_manager.check_valve_cycle_running():
                delay = self.__get_delay(appointment['timestamp'])
                duration = appointment['duration']
                self.__valve_manager.start_valves_cycle(duration*60, delay)
                copy_of_appointment = appointment

        self.__valve_manager.stop_valves_cycle()



    def __get_delay(self, timestamp):
        return int(timestamp - datetime.datetime.now().timestamp())

    def __sleep(self, secs):
        while secs >= 0:
            secs -= 1
            time.sleep(1)
            if not self.running:
                return False
        return True

    def is_running(self):
        return self.running