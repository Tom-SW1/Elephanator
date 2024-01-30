import json
from datetime import datetime
from typing import Union

from Logic.Cryptography import Cryptography
from Logic.Conversion import Conversion
from Logic.Sort import Sort

class PatchesSignature:
    @staticmethod
    def hasDifferentSignature() -> bool:
        """
        Compares the signature in patches.signature.json with the current signature of patches.json
        :return:
        """
        # Get the signature from patches.signature.json
        with open('patches.signature.json', 'r') as f:
            signature = json.load(f)['signature']

        # Get the signature from patches.json
        newSignature = Cryptography.hashFile('patches.json')

        # Compare the signatures
        return signature != newSignature

    @staticmethod
    def updateSignature(lastInsert: Union[int, None] = None) -> None:
        """
        Updates the signature and timestamps in patches.signature.json
        :return:
        """
        try:
            # Get the timestamp from patches.signature.json
            with open('patches.signature.json', 'r') as f:
                stamp = json.load(f)['timestamp']
        except FileNotFoundError:
            # If the file does not exist then set the timestamp to the current time
            stamp = int(round(datetime.timestamp(datetime.now()) * 1000, 0))

        # If the last insert is None then set it to the current timestamp
        if lastInsert is None:
            lastInsert = int(round(datetime.timestamp(datetime.now()) * 1000, 0))

        # Update the timestamp and signature in patches.signature.json
        with open('patches.signature.json', 'w') as f:
            json.dump({
                'timestamp': stamp,
                'lastLocalInsert': lastInsert,
                'signature': Cryptography.hashFile('patches.json')
            }, f)

    @staticmethod
    def updateSignatureWithSort() -> None:
        """
        Updates the signature and sorts new patches
        :return:
        """
        # Get the patches from patches.json
        with open('patches.json', 'r') as f:
            patches = json.load(f)['patches']

        # Get the timestamp from patches.signature.json
        with open('patches.signature.json', 'r') as f:
            signature = json.load(f)

        # If both timestamps are the same then sort all patches as the original signature was blank
        if signature['timestamp'] == signature['lastLocalInsert']:
            patches = Sort.patch(patches)
        else:
            # Use the timestamps to find the cutoff point for the patches
            cutoff = None
            # first find the cutoff for the last local insert
            for patch in patches:
                if Conversion.fromHexPatchStamp(patch['id']) == signature['lastLocalInsert']:
                    cutoff = patches.index(patch)

            # Now from this point use the timestamp to find the cutoff for the signature, but only run if the
            # timestamp is less than the local insert timestamp
            if signature['timestamp'] < signature['lastLocalInsert']:
                for patch in patches[cutoff:]:
                    if Conversion.fromHexPatchStamp(patch['id']) <= signature['timestamp']:
                        cutoff = patches.index(patch)
                        break

            # Ensure that a cutoff was found
            if cutoff is None:
                raise Exception('Malformed Patches: could not find cutoff for patches!')

            newPatches = patches[:cutoff][:-1]

            # If there are no new patches then return
            if len(newPatches) == 0:
                return

            # Sort the patches, starting with the patches which are not larger than the original signature timestamp
            insertPatches = Sort.patchWithInsert(newPatches, patches[cutoff:], signature['timestamp'])

            newPatches = Sort.patch(newPatches)

            # Prepend the new patches to the sorted patches
            patches = newPatches + insertPatches

        # Update the patches.json file
        with open('patches.json', 'w') as f:
            json.dump({
                'patches': patches
            }, f)

        # Update the signature
        with open('patches.signature.json', 'w') as f:
            json.dump({
                'timestamp': int(round(datetime.timestamp(datetime.now()) * 1000, 0)),
                'lastLocalInsert': Conversion.fromHexPatchStamp(patches[0]['id']),
                'signature': Cryptography.hashFile('patches.json')
            }, f)