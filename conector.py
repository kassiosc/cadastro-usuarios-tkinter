import mysql.connector
from mysql.connector import Error

import config


class Conector:
    def __init__(self):
        self.host = config.DB_HOST
        self.database = config.DB_NAME
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD

    def conectar(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
        except Error as erro:
            print(f"Erro ao conectar ao MySQL: {erro}")
            return None
