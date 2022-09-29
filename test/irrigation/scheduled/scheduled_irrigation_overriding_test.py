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
    duration = 1
    # create another instance that should start 3 seconds after the first one, with the same duration
    in_8_seconds = datetime.datetime.now() + datetime.timedelta(seconds=8)

    #Act
    user.create_schedule(in_5_seconds.timestamp(), duration)
    # scheduling it
    user.create_schedule(in_8_seconds.timestamp(), duration)
    scheduled_irrigation.start()
    time.sleep(1)

    #Assert
    assert scheduled_irrigation.is_running() == True

    #the first irrigation should end at 12s point, the second assert here should mark 1+12s point
    time.sleep(12)
    assert scheduled_irrigation.is_running() == False

