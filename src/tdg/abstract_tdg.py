import sqlite3
import os


class DatabaseEnum:
    CONCORDIA = r'database/concordia-data.sqlite'
    TIM_HORTONS = r'database/timhortons-data.sqlite'
    HOME = r'database/home-data.sqlite'

    def __init__(self):
        pass


class AbstractTdg:
    __root_directory = os.path.abspath(__file__ + "r/../../")

    def __init__(self, database):
        self.connection = None
        self.DATABASE = os.path.join(self.__root_directory, database)

    def connect(self):
        self.connection = sqlite3.connect(self.DATABASE)

    def disconnect(self):
        self.connection.close()

    def select(self):
        raise NotImplementedError
