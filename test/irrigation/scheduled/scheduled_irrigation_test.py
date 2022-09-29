import pytest
import time
import datetime
from is_iot_sink.irrigation.irrigation_mode import *
from is_iot_sink.irrigation.scheduled.scheduled_irrigation import ScheduledIrrigation
from is_iot_sink.irrigation.valves.valves_manager import ValveManager
from is_iot_sink.mongodb.mongodb_client import MongoClient
from is_iot_sink.settings import Settings
from test.mocks.user_mock import UserMock
from test.helper import TestHelper

def setup_module():
    TestHelper.suite_setup()

def teardown_module():
    TestHelper.suite_teardown()

def setup_method():
    TestHelper.cleanup_database()

def test_starts_valve_cycle():
    # Arrange
    settings = Settings(TestHelper.fixture_path('scheduled_irrigation_initial_mode_setup.yml'))
    mongo_client = MongoClient(settings)
    user = UserMock(settings, mongo_client)
    valve_manager = ValveManager(settings, mongo_client)
    scheduled_irrigation = ScheduledIrrigation(valve_manager, mongo_client)
    in_5_seconds = datetime.datetime.now() + datetime.timedelta(seconds=5)
    duration = 5

    #Act
    user.create_schedule(in_5_seconds.timestamp(), duration)
    scheduled_irrigation.start()
    time.sleep(1)

    #Assert
    assert scheduled_irrigation.is_running() == True

    time.sleep(30)
    assert scheduled_irrigation.is_running() == False

