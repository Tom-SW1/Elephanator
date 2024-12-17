import os
import json

from Data.DataHelper import DataHelper
from Logic.Patches import Patches


class Initialisation:
    @staticmethod
    def connection_string(connection_string: str) -> None:
        """
        Writes the connection string to the appsettings.json file
        :param connection_string: The connection string
        :return: None
        """
        # Check the connection string is valid to postgres
        if 'host=' not in connection_string:
            raise Exception(
                'Invalid connection string! Must contain: host=<host>')
        if 'dbname=' not in connection_string:
            raise Exception(
                'Invalid connection string! Must contain: dbname=<database name>')
        if 'user=' not in connection_string:
            raise Exception(
                'Invalid connection string! Must contain user=<username>')
        if 'password=' not in connection_string:
            raise Exception(
                'Invalid connection string! Must contain: password=<password>')
        if 'port=' not in connection_string:
            raise Exception(
                'Invalid connection string! Must contain: port=<port>')

        # Write the connection string to the appsettings.json file
        with open('appsettings.json', 'w') as f:
            json.dump({'connectionString': connection_string}, f)

    @staticmethod
    def execute() -> None:
        """
        Initialises the database tool
        :return: None
        """
        # Check the appsettings.json file exists
        if not os.path.exists('appsettings.json'):
            raise Exception(
                'No appsettings.json file found! Run: python dbtool.py --init --connectionstring <connection string>')

        # Check the appsettings.json file has a connection string
        with open('appsettings.json', 'r') as f:
            appsettings = json.load(f)
            if 'connectionString' not in appsettings:
                raise Exception(
                    'No connection string found! Add one using: python dbtool.py --init --connectionstring <connection string>')

        # Insert the installed_patches table if it doesn't exist
        dh = DataHelper()
        dh.execute('CREATE TABLE IF NOT EXISTS installed_patches (patch_id TEXT PRIMARY KEY, patch_date TIMESTAMPTZ NOT NULL);')

        # Create patches directory if it doesn't exist
        if not os.path.exists('patches'):
            os.makedirs('patches')

        # Create patches.json if it doesn't exist
        if not os.path.exists('patches.json'):
            with open('patches.json', 'w') as f:
                f.write('{"patches": []}')

        # Order the patches
        Patches.sort_patches()
