import json

from Models import InitSystemSchema
from Logic.ArgumentFactory import ArgumentFactory

class Init:
    @staticmethod
    def execute(data: dict[str, dict[list[str]]]) -> None:
        """
        Initializes the basic settings of the system
        :param data: The data to use to initialize the system
        :return:
        """
        # Format the arguments, also validates the arguments using the schema
        args = ArgumentFactory.format(InitSystemSchema.schema, data['arguments'])

        # Get the database connection string from the arguments
        connectionString = args['connectionstring']

        # Create the database connection string
        if not(';' in connectionString):
            # If there is no semicolon then it must be invalid
            raise Exception('Invalid connection string\ntip: you may need to wrap it in quotes')

        # Update the appsettings.json file with the connection string, or create it if it doesn't exist
        with open('appsettings.json', 'w') as f:
            f.write('{' + f'"connectionString": "{connectionString}"' + '}')
