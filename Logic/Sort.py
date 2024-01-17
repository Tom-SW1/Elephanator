from typing import Union
from collections import deque

from Logic.Search import Search

class Sort:
    @staticmethod
    def patch(patches: list[dict[str, Union[str, list[str]]]]) -> list[dict[str, Union[str, list[str]]]]:
        """
        Sorts patches which are not larger than the original signature timestamp using timsort
        :param patches: The patches to sort
        :return: The sorted patches
        """
        # If there is only one patch then return it
        if len(patches) == 1:
            return patches

        # Create a list of timestamps
        timestamps = []
        for patch in patches:
            timestamps.append(int(bytes.fromhex(patch['id'].split('-')[0]).decode('utf-8')))

        # Sort the timestamps using timsort
        timestamps.sort()

        # Create a list of patches using the sorted timestamps
        sortedPatches = []
        for timestamp in timestamps:
            for patch in patches:
                if int(bytes.fromhex(patch['id'].split('-')[0]).decode('utf-8')) == timestamp:
                    sortedPatches.append(patch)
                    break

        # Return the sorted patches
        return sortedPatches

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
            newStamp = int(bytes.fromhex(newPatch['id'].split('-')[0]).decode('utf-8'))
            # If the is less than the original signature timestamp then insert it into the existing patches
            if newStamp < stamp:
                # Get the range of the existing patches to search
                position = Search.forInsert(patches.copy(), newStamp)

                # Insert the new patch into the existing patches
                existingPatches.insert(position[1], newPatch)

                # Remove the new patch from the new patches
                newPatches.remove(newPatch)

        # Convert the deque back to a list and return it
        return list(existingPatches)