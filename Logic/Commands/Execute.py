import os

from Data.DataHelper import DataHelper
from Logic.ArgumentFactory import ArgumentFactory

class Execute:
    @staticmethod
    def run() -> None:
        """
        Runs patches that haven't been executed yet
        :return:
        """
        # Check that a connection string has been provided
        if os.getenv('connectionString') is None:
            raise Exception('No connection string found! Add one using: python dbtool.py --init --connectionstring <connection string>')

        # Build the datahelper using the connection string
        db = DataHelper(os.getenv('connectionString'))