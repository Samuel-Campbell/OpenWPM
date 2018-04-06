import sqlite3
import os


class AbstractTdg:
    __root_directory = os.path.abspath(__file__ + "r/../../")
    __rel_path = r'database/concordia-data.sqlite'
    DATABASE = os.path.join(__root_directory, __rel_path)

    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(AbstractTdg.DATABASE)

    def disconnect(self):
        self.connection.close()

    def select(self):
        raise NotImplementedError
