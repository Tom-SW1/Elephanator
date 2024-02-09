import math
from typing import Union

from Data.InstalledPatchesRepository import InstalledPatchesRepository
from Logic.Conversion import Conversion

class Search:
    db = InstalledPatchesRepository()

    @staticmethod
    def forInsert(patches: list[dict[str, Union[str, list[str]]]], stamp: int) -> Union[tuple[dict[str, Union[str,
    list[str]]], dict[str, Union[str, list[str]]]], None]:
        """
        Searches for the range of patches to insert a new patch into
        :param patches: The patches to search
        :param stamp: The timestamp of the new patch
        :return: The two patches to insert the new patch between
        """
        midpoint = int(math.ceil(len(patches) / 2)) - 1

        # Get the patch at the midpoint and its timestamp
        patch = patches[midpoint]
        timestamp = Conversion.fromHexPatchStamp(patch['id'])

        # If the timestamp is equal to the stamp then there is a conflict
        if timestamp == stamp:
            raise Exception(f'Patch Conflict: {patch["id"]} already uses this timestamp!')
        # If there are two patches left then we can return that as our range
        elif len(patches) == 2:
            return patches[0], patches[1]
        # If there is just one patch left then we return None as it goes to the end of the list
        elif len(patches) == 1:
            return None
            # If the stamp is less than the timestamp then search the right side of the list
        elif stamp < timestamp:
            patches = patches[midpoint:]
            return Search.forInsert(patches, stamp)
        # If the stamp is greater than the timestamp then search the left side of the list
        elif stamp > timestamp:
            patches = patches[:midpoint]
            return Search.forInsert(patches, stamp)

    @staticmethod
    def forPatch(patches: list[dict[str, Union[str, list[str]]]], stamp: int) -> Union[
        dict[str, Union[str, list[str]]], None]:
        """
        Searches for a patch using a timestamp
        :param patches:
        :param stamp:
        :return:
        """
        midpoint = int(math.ceil(len(patches) / 2)) - 1

        # Get the patch at the midpoint and its timestamp
        patch = patches[midpoint]
        timestamp = Conversion.fromHexPatchStamp(patch['id'])

        # If the timestamp is equal to the stamp then return the patch
        if timestamp == stamp:
            return patch
        # If there are two patches left then check the one that wasn't just checked
        elif len(patches) == 2:
            if midpoint == 0:
                patch = patches[1]
            else:
                patch = patches[0]
            timestamp = Conversion.fromHexPatchStamp(patch['id'])
            if timestamp == stamp:
                return patch
        # If the stamp is less than the timestamp then search the right side of the list
        elif stamp < timestamp:
            patches = patches[midpoint:]
            return Search.forPatch(patches, stamp)
        # If the stamp is greater than the timestamp then search the left side of the list
        elif stamp > timestamp:
            patches = patches[:midpoint]
            return Search.forPatch(patches, stamp)

        # If the patch is not found then return None
        return None

    @staticmethod
    def forDependencies(patches: list[dict[str, Union[str, list[str]]]], patch: str, execution: list[str] = []) -> list[str]:
        """
        Searches for the dependencies of a patch
        :param patches:
        :param patch:
        :param execution:
        :return:
        """
        patchInfo = Search.forPatch(patches, Conversion.fromHexPatchStamp(patch))

        # If the patch is not found then raise an exception
        if patchInfo is None:
            raise Exception(f'Patch does not exist: {patch}')

        # Check if the patch has already been executed
        if Search.db.select(patch) is not None:
            return execution

        # Prepend to the execution list
        execution = patchInfo['dependencies'] + execution

        # If there are no more dependencies than return the execution list
        if len(patchInfo['dependencies']) == 0:
            return execution

        # Recurse through the dependencies
        for dependency in patchInfo['dependencies']:
            execution = Search.forDependencies(patches, dependency, execution)