import datetime

from is_iot_sink.irrigation.irrigation_mode import *
from is_iot_sink.irrigation.valves.valves_manager import ValveManager
from is_iot_sink.mongodb.mongodb_client import MongoClient
from is_iot_sink.settings import Settings
from is_iot_sink.logger import LOG
import time
import threading


class ScheduledIrrigation:
    RAIN_PROB_THRESHOLD = 75
    def __init__(self, valve_manager: ValveManager, mongo_client: MongoClient):
        self.__valve_manager = valve_manager
        self.__mongo_client = mongo_client
        self.mode = IrrigationMode.SCHEDULED
        self.running = False
        self.global_thread = threading.Thread(target=self.__run, daemon=True)
        self.weather = Weather(self.__settings.get("location/latitude"), self.__settings.get("location/longitude"))
        self.__email_sent = False

    def start(self):
        LOG.info("Scheduled Irrigation process started.")
        self.running = True
        self.global_thread.start()

    def stop(self):
        LOG.info("Scheduled Irrigation process stopped.")
        self.running = False
        self.global_thread.join()

    def __rain_probability(self):
        return self.weather.get_1hour_data()[0]["RainProbability"]

    def __run(self):
        appointment = None
        copy_of_appointment = None

        while self.running:
            appointment = self.__mongo_client.read_first_appointment()

            if appointment and copy_of_appointment != appointment and not self.__valve_manager.check_valve_cycle_running():
                delay = self.__get_delay(appointment['timestamp'])
                duration = appointment['duration']
                self.__valve_manager.start_valves_cycle(duration*60, delay)
                self.__email_sent = False
                copy_of_appointment = appointment

            if appointment:
                if self.__is_raining_next_hour(appointment) and self.__email_sent == False:
                    self.__send_mail()
                    self.__email_sent = True


        self.__valve_manager.stop_valves_cycle()


    def __send_mail(self):
        users = self.__mongo_client.get_users_id_for_sink(self.__settings.get('sinkId'))
        emails = [self.__mongo_client.get_user_email(user) for user in users]
        msg ="""The weather shows that a probability of rain higher than 75% in the next hour, and you have an irrigation schedule set.
                You should consider cancelling this schedule appointment.
              """
        mail = Mailer()
        mail.send_mail_for_rain_probability(emails, msg)


    def __is_raining_next_hour(self, appointment):
        current_timestamp = datetime.datetime.now().timestamp()
        appointment_timestamp = appointment['timestamp']
        next_hours_timestamp = current_timestamp + 3600

        if current_timestamp < appointment_timestamp < next_hours_timestamp:
            probability = self.__rain_probability()

            if probability > self.RAIN_PROB_THRESHOLD:
                return True


        return False

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