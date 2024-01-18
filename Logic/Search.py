import math
from typing import Union


class Search:
    @staticmethod
    def forInsert(patches: list[dict[str, Union[str, list[str]]]], stamp: int) -> Union[tuple[dict[str, Union[str,
    list[str]]], dict[str, Union[str, list[str]]]], None]:
        """
        Searches for the range of patches to insert a new patch into
        :param patches: The patches to search
        :param stamp: The timestamp of the new patch
        :return: The two patches to insert the new patch between
        """
        midpoint = int(math.ceil(len(patches) / 2))

        # Get the patch at the midpoint and its timestamp
        patch = patches[midpoint]
        timestamp = int(bytes.fromhex(patch['id'].split('-')[0]).decode('utf-8'))

        # If the timestamp is equal to the stamp then there is a conflict
        if timestamp == stamp:
            raise Exception(f'Patch Conflict: {patch["id"]} already uses this timestamp!')
        # If the timestamp is less than the stamp then search the right side of the list
        elif timestamp < stamp:
            patches = patches[midpoint:]
            return Search.forInsert(patches, stamp)
        # If the timestamp is greater than the stamp then search the left side of the list
        elif timestamp > stamp:
            patches = patches[:midpoint]
            return Search.forInsert(patches, stamp)
        # If there are two patches left then we can return that as our range
        elif len(patches) == 2:
            return patches[0], patches[1]
        # If there is just one patch left then we return None as it goes to the end of the list
        elif len(patches) == 1:
            return None

    @staticmethod
    def forPatch(patches: list[dict[str, Union[str, list[str]]]], stamp: int) -> Union[
        dict[str, Union[str, list[str]]], None]:
        midpoint = int(math.ceil(len(patches) / 2))

        # Get the patch at the midpoint and its timestamp
        patch = patches[midpoint]
        timestamp = int(bytes.fromhex(patch['id'].split('-')[0]).decode('utf-8'))

        # If the timestamp is equal to the stamp then return the patch
        if timestamp == stamp:
            return patch
        # If the timestamp is less than the stamp then search the right side of the list
        elif timestamp < stamp:
            patches = patches[midpoint:]
            return Search.forPatch(patches, stamp)
        # If the timestamp is greater than the stamp then search the left side of the list
        elif timestamp > stamp:
            patches = patches[:midpoint]
            return Search.forPatch(patches, stamp)
        # If there are two patches left then check the one that wasn't just checked
        elif len(patches) == 2:
            patch = patches[0]
            timestamp = int(bytes.fromhex(patch['id'].split('-')[0]).decode('utf-8'))
            if timestamp == stamp:
                return patch

        # If the patch is not found then return None
        return None
