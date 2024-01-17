import json
import os

from Logic.ArgumentFactory import ArgumentFactory
from Logic.Cryptography import Cryptography
from Models import AddPatchSchema


class Patch:
    @staticmethod
    def add(data: dict[str, dict[list[str]]]) -> None:
        """
        Adds a new patch to the patches directory
        :param data: The data to add the patch
        :return:
        """
        # Format the arguments, also validates the arguments using the schema
        args = ArgumentFactory.format(AddPatchSchema.schema, data['arguments'])

        # Remove whitespace from the name
        args['name'] = args['name'].replace(' ', '_')

        # Check if the patch already exists
        patch = ArgumentFactory.locatePatch(args['name'])
        if patch is not None:
            raise Exception(f'Patch directory already exists: {args["name"]} -> {patch}')

        # Create an ID for the patch
        identifier = f'{Cryptography.createID()}-{args["name"]}'

        # Create the patch directory
        os.makedirs(f'patches/{identifier}')

        # Append the patch to patches.json
        with open('patches.json', 'r') as f:
            patches = json.load(f)
            patches['patches'].append({
                'id': identifier,
                'dependencies': []
            })

        with open('patches.json', 'w') as f:
            json.dump(patches, f)
