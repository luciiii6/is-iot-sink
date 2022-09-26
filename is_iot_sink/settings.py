from threading import Lock
import yaml
import dpath.util
import os

DEFAULT_PATH = os.getenv('PROJECT_PATH') + '/setup.yml'

class Settings:
    def __init__(self, filepath = DEFAULT_PATH, mutex = Lock()):
        file = open(filepath)
        self.__settings = yaml.safe_load(file)
        self.__mutex = mutex

    def get(self, name):
        with self.__mutex:
            value = dpath.util.get(self.__settings, name)

        return value

    def set(self, name, value):
        with self.__mutex:
            dpath.util.set(self.__settings, name, value)
