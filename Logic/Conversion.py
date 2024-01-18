class Conversion:
    @staticmethod
    def fromHexPatchStamp(patch: str) -> int:
        """
        Converts the hex timestamp within a patch to an integer
        :param patch: The patch to convert
        :return: The converted timestamp
        """
        stamp = patch.split('-')[0]

        return int(stamp, 16)