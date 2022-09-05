import subprocess
import os
from dotenv import Dotenv
from pathlib import Path
from is_iot_sink.mongodb.mongodb_test_client import MongoTestClient

class TestHelper:
    @classmethod
    def suite_setup(self):
        self.__set_environment_variables()
        self.__start_local_mqtt_broker()
        self.__start_local_mongodb()

    @classmethod
    def suite_teardown(self):
        self.__stop_local_mqtt_broker()
        self.__stop_local_mongodb()

    @classmethod
    def test_setup(self):
        MongoTestClient().clean_up()

    @classmethod
    def test_teardown(self):
        MongoTestClient().clean_up()

    @classmethod
    def __start_local_mqtt_broker(self):
        subprocess.run('sudo service mosquitto start'.split(), stdout=subprocess.DEVNULL)

    @classmethod
    def __stop_local_mqtt_broker(self):
        subprocess.run('sudo service mosquitto stop'.split(), stdout=subprocess.DEVNULL)

    @classmethod
    def __start_local_mongodb(self):
        subprocess.run('sudo service mongodb start'.split(), stdout=subprocess.DEVNULL)

    @classmethod
    def __stop_local_mongodb(self):
        subprocess.run('sudo service mongodb stop'.split(), stdout=subprocess.DEVNULL)

    @classmethod
    def __set_environment_variables(self):
        env_file_path = Path(os.getenv('PROJECT_PATH') + '/.env.test')
        dotenv = Dotenv(env_file_path)
        os.environ.update(dotenv)
