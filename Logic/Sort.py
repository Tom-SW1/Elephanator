from typing import Union
from collections import deque

from Logic.Search import Search

class Sort:
    @staticmethod
    def patch(patches: list[dict[str, Union[str, list[str]]]]) -> list[dict[str, Union[str, list[str]]]]:
        """
        Sorts patches which are not larger than the original signature timestamp using merge sort
        :param patches: The patches to sort
        :return: The sorted patches
        """
        pass

    @staticmethod
    def patchWithInsert(newPatches: list[dict[str, Union[str, list[str]]]], patches: list[dict[str, Union[str,
        list[str]]]], stamp: int) -> list[dict[str, Union[str, list[str]]]]:
        """
        Sorts patches which are not larger than the original signature timestamp using insertion sort
        :param newPatches: The patches to sort
        :param patches: The existing patches which are already sorted
        :param stamp: The timestamp of the original signature
        :return: The sorted patches
        """
        # Convert the list of existing patches to a deque
        existingPatches = deque(patches)

        for newPatch in newPatches:
            pass

        # Convert the deque back to a list and return it
        return list(existingPatches)