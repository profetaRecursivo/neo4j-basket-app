import tomllib
from neo4j import GraphDatabase, Session
import random
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DBManager(metaclass=SingletonMeta):
    def __init__(self, config_file="credential.toml"):
        with open(config_file, "rb") as f:
            data = tomllib.load(f)

        cfg = data["neo4j"]

        uri = cfg["host"]
        user = cfg["user"]
        password = cfg["password"]
        
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_session(self, **kwargs):
        return self._driver.session(**kwargs)

    def close(self):
        self._driver.close()
    def get_pid(self):
        return random.randrange(1, 10000000000) 