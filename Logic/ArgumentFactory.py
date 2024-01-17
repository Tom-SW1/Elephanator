import os
import json
from typing import Union

from Logic.Search import Search

class ArgumentFactory:
    @staticmethod
    def format(schema: dict[str, dict[Union[type[any], bool]]], args: dict[list[str]]) -> dict:
        pass

    @staticmethod
    def locatePatch(name: str) -> Union[str, None]:
        """
        Locates a patch using its name in the patches directory using linear search
        :param name: The name of the patch to locate
        :return: The patch or None
        """
        for patch in os.listdir('patches'):
            if patch.endswith(name):
                return patch

    @staticmethod
    def findCircularDependency(self, patch: str, dependencies: list[str], source: list[str] = []) -> Union[str, None]:
        """
        Finds a circular dependency in a patch
        :param self:
        :param patch: The patch to check
        :param dependencies: The dependencies of the original patch
        :param source: The source list of dependencies
        :return: The circular dependency or None
        """

        # If the source list is empty then set it to the dependencies list by duplicating it
        isStart = False
        if len(source) == 0:
            source = dependencies.copy()
            isStart = True

        # Get all patches from patches.json
        with open('patches.json', 'r') as f:
            patches = json.load(f)['patches']

        for dependency in source:
            # Get the timestamp for the patch
            stamp = int(bytes.fromhex(dependency.split('-')[0]).decode('utf-8'))

            # Check if the patch is in the dependencies list, but ensure it is not the patch it is checking
            if not isStart:
                if dependency in dependencies:
                    # If it is in the dependencies list then there is a circular dependency
                    return dependency

            # Search for the patch
            patchInfo = Search.forPatch(patches.deepcopy(), stamp)

            # Check if the patch exists
            if patchInfo is None:
                raise Exception(f'Dependency does not exist for a patch: {patch} depends on {dependency}')

            # Set the patch name to the identifier
            patch = patchInfo['id']

            # If the patch has no dependencies then return None
            if len(patchInfo['dependencies']) == 0:
                return None

            # Check if there is a circular dependency
            source = patchInfo['dependencies']
            return self.findCircularDependency(patch, patchInfo['dependencies'], source)