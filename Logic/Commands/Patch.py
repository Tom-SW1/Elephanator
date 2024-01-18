import json
import os

from Logic.ArgumentFactory import ArgumentFactory
from Logic.Cryptography import Cryptography
from Logic.PatchesSignature import PatchesSignature
from Logic.Conversion import Conversion
from Models import AddPatchSchema


class Patch:
    @staticmethod
    def add(data: dict[str, dict[str, list[str]]]) -> None:
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

        # Check if the patch has any dependencies
        dependencies = []
        if 'dependencies' in args:
            for dependency in args['dependencies']:
                # Check if the dependency is already in the list
                if dependency in dependencies:
                    raise Exception(f'Dependency already exists: {dependency}')

                # Check if the dependency exists
                patch = ArgumentFactory.locatePatch(dependency)
                if patch is None:
                    raise Exception(f'Patch directory does not exist: {dependency}')

                # Add the dependency to the list
                dependencies.append(patch)

            # Check if there are any circular dependencies
            circularDependency = ArgumentFactory.findCircularDependency(identifier, dependencies)
            if circularDependency is not None:
                raise Exception(f'Patch would create a circular dependency: {circularDependency}')

        # Create the patch directory
        os.makedirs(f'patches/{identifier}')

        # Append the patch to patches.json
        with open('patches.json', 'r') as f:
            patches = json.load(f)
            patches['patches'] = [{'id': identifier, 'dependencies': dependencies}] + patches['patches']

        with open('patches.json', 'w') as f:
            json.dump(patches, f)

        # Update the signature
        PatchesSignature.updateSignature(Conversion.fromHexPatchStamp(identifier))
