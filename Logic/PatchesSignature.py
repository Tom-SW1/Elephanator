import json
from datetime import datetime

from Logic.Cryptography import Cryptography

class PatchesSignature:
    @staticmethod
    def hasDifferentSignature() -> bool:
        # Get the signature from patches.signature.json
        with open('patches.signature.json', 'r') as f:
            signature = json.load(f)['signature']

        # Get the signature from patches.json
        newSignature = Cryptography.hashFile('patches.json')

        # Compare the signatures
        return signature != newSignature

    @staticmethod
    def updateSignature() -> None:
        try:
            # Get the timestamp from patches.signature.json
            with open('patches.signature.json', 'r') as f:
                stamp = json.load(f)['timestamp']
        except FileNotFoundError:
            # If the file does not exist then set the timestamp to the current time
            stamp = int(round(datetime.timestamp(datetime.now()) * 1000, 0))

        # Update the timestamp and signature in patches.signature.json
        with open('patches.signature.json', 'w') as f:
            json.dump({
                'timestamp': stamp,
                'signature': Cryptography.hashFile('patches.json')
            }, f)

    @staticmethod
    def updateSignatureWithSort() -> None:
        pass