from datetime import datetime
from hashlib import sha256


class Cryptography:

    @staticmethod
    def createID() -> str:
        """
        Gets the current timestamp in milliseconds and converts it to hex to form an ID
        :return: A hex of current datetime
        """
        timestamp = hex(int(datetime.timestamp(datetime.now()) * 1000))[2:]

        return f'{timestamp}'

    @staticmethod
    def hashFile(path: str) -> str:
        """
        Hashes the contents of a defined file
        :argument path: The path to a file
        :return: A SHA-256 hash of the contents of a file
        """

        # Read the contents of the file
        with open(path, 'r') as file:
            data = file.read()

        return sha256(data.encode('utf-8')).hexdigest()
