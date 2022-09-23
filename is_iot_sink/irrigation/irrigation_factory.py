from is_iot_sink.irrigation.manual.manual_irrigation import ManualIrrigation
from is_iot_sink.irrigation.automated.automted_irrigation import AutomatedIrrigation
from is_iot_sink.irrigation.mode import *
from is_iot_sink.irrigation.valves.valves_manager import ValveManager
from is_iot_sink.mongodb.mongodb_client import MongoClient
from is_iot_sink.settings import Settings

class IrrigationFactory:
    def __init__(self, settings: Settings, valve_manager: ValveManager, mongo_client: MongoClient):
        self.__settings = settings
        self.__valve_manager = valve_manager
        self.__mongo_client = mongo_client

    def create(self, mode):
        if (mode == Mode.MANUAL):
            return ManualIrrigation()
        elif (mode == Mode.AUTO):
            return AutomatedIrrigation(self.__settings, self.__valve_manager, self.__mongo_client)
        else:
            return None
