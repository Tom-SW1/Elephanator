import json
import psycopg2

from typing import Union


class DataHelper:
    def __init__(self):
        # Get connection string from app settings
        with open('appsettings.json', 'r') as f:
            data = json.load(f)
            connectionString = data['connectionString']

        # Connect to the database
        self.conn = psycopg2.connect(connectionString.replace(';', ' '))
        self.conn.autocommit = False
        self.db = self.conn.cursor()

    def selectFirstWithParams(self, query: str, params: tuple) -> Union[tuple, None]:
        self.db.execute(query, params)
        return self.db.fetchone()

    def execute(self, query: str, params: tuple = ()) -> None:
        self.db.execute(query, params)

    def commit(self):
        self.conn.commit()