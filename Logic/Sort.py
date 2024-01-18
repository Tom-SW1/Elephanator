import copy
from typing import Union
from collections import deque

from Logic.Search import Search
from Logic.Conversion import Conversion

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
            timestamps.append(Conversion.fromHexPatchStamp(patch['id']))

        # Sort the timestamps using timsort
        timestamps.sort(reverse=True)

        # Create a list of patches using the sorted timestamps
        sortedPatches = []
        for timestamp in timestamps:
            for patch in patches:
                if Conversion.fromHexPatchStamp(patch['id']) == timestamp:
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
            newStamp = Conversion.fromHexPatchStamp(newPatch['id'])
            # If the is less than the original signature timestamp then insert it into the existing patches
            if newStamp < stamp:
                # Get the range of the existing patches to search
                patch = Search.forInsert(copy.deepcopy(patches), newStamp)

                # Check if the patch should be appended to the end of the existing patches
                if patch is None:
                    existingPatches.append(newPatch)
                # Insert the new patch into the existing patches
                else:
                    existingPatches.insert(existingPatches.index(patch[1]), newPatch)

                # Remove the new patch from the new patches
                newPatches.remove(newPatch)

        # Convert the deque back to a list and return it
        return list(existingPatches)