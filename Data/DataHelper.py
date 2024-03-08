import json
import psycopg2

from typing import Union


class DataHelper:
    def __init__(self):
        # Get connection string from app settings
        connectionString = None
        try:
            with open('appsettings.json', 'r') as f:
                appsettings = json.load(f)
                connectionString = appsettings['connectionString'].replace(';', ' ')
        except:
            pass

        # If it doesn't exist throw an error
        if connectionString is None:
            raise Exception('No connection string found! Add one using: python dbtool.py --init --connectionstring <connection string>')

        # Connect to the database
        conn = psycopg2.connect(connectionString)
        conn.autocommit = True
        self.db = conn.cursor()

    def selectFirstWithParams(self, query: str, params: tuple) -> Union[tuple, None]:
        self.db.execute(query, params)
        return self.db.fetchone()

    def execute(self, query: str, params: tuple) -> None:
        self.db.execute(query, params)