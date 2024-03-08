import os
import json
from datetime import datetime

from Data.DataHelper import DataHelper
from Data.InstalledPatchesRepository import InstalledPatchesRepository
from Models import ExecutePatchesSchema
from Logic.ArgumentFactory import ArgumentFactory
from Logic.Search import Search

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
        installedPatchesRepository = InstalledPatchesRepository()
        db = DataHelper()

        # Create the InstalledPatches table if it doesn't exist
        installedPatchesRepository.build()

        # Read the patches.json file
        with open('patches.json', 'r') as f:
            patches = json.load(f)['patches']

        # Get the patches that haven't been executed
        execution = []

        # Check if only one patch is to be executed
        if 'patch' in args:
            patch = installedPatchesRepository.select(args['patch'])

            # Check if the patch has already been executed
            if not (patch is None):
                raise Exception(f'Patch has already been executed -> {args["patch"]}')

            # Check if the patch exists
            if not(patch in os.listdir('patches')):
                raise Exception(f'Patch does not exist -> {args["patch"]}')

            execution = Search.forDependencies(patches, args['patch'])
        # Find all the patches that haven't been executed
        else:
            for patch in patches:
                if installedPatchesRepository.select(patch['id']) is None:
                    execution = Search.forDependencies(patches, patch['id'], execution)

        # Execute the patches
        for patch in execution:
            # Check if the patch has been executed
            if installedPatchesRepository.select(patch) is not None:
                print(f'Patch requirement already satisfied -> {patch}')

            # Execute the patch
            print(f'Executing patch -> {patch}')

            # Get files within the patch
            files = os.listdir(f'patches/{patch}')

            # Execute the files in the patch
            for file in files:
                try:
                    with open(f'patches/{patch}/{file}', 'r') as f:
                        query = f.read()

                    # Split the query into individual queries
                    queries = query.split(';')
                    for q in queries:
                        db.execute(q + ";")
                except Exception as e:
                    print(f'Error executing file: {patch}/{file} -> {e}')

            # Insert the patch into the InstalledPatches table
            installedPatchesRepository.insert(patch, int(datetime.timestamp(datetime.now()) * 1000))

            # Notify the user that the patch has been executed
            print(f'Patch executed -> {patch}')

        # Notify the user that the patches have been executed
        print('All patches executed!')