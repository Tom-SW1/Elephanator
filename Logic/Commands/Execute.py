import os
import json

from Data.DataHelper import DataHelper
from Models import ExecutePatchesSchema
from Logic.ArgumentFactory import ArgumentFactory

class Execute:
    @staticmethod
    def run(data: dict[str, dict[list[str]]]) -> None:
        """
        Runs patches that haven't been executed yet
        :return:
        """
        # Format the arguments, also validates the arguments using the schema
        args = ArgumentFactory.format(ExecutePatchesSchema.schema, data['arguments'])

        # Check that a connection string has been provided
        if os.getenv('connectionString') is None:
            raise Exception('No connection string found! Add one using: python dbtool.py --init --connectionstring <connection string>')

        # Build the datahelper using the connection string
        db = DataHelper(os.getenv('connectionString'))

        # Read the patches.json file
        with open('patches.json', 'r') as f:
            patches = json.load(f)['patches']

        # Get the patches that haven't been executed


        # Check if only one patch is to be executed
        if 'patch' in args:
            patch = db.getPatch(args['name'])