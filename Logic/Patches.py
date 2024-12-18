from datetime import datetime
import json

from Data.DataHelper import DataHelper


class Patches:
    @staticmethod
    def create_patch(patch_name: str) -> None:
        """
        Creates a new patch file and adds it to the patches.json file
        :param patch_name: The name of the patch
        :return: None
        """
        # Replace whitespace with underscores
        patch_name = patch_name.replace(' ', '_')

        # Get patch timestamp
        timestamp = int(datetime.timestamp(datetime.utcnow()) * 1000)

        # Convert timestamp to hex string to use as patch id
        patch_id = hex(timestamp)[2:]

        # Create the patch file
        with open(f'patches/{patch_id}_{patch_name}.sql', 'w') as f:
            f.write('-- Write your patch here')

        # Open the patches.json file
        with open('patches.json', 'r') as f:
            data = json.load(f)

        # Add the patch to the patches.json file
        data['patches'].append({
            'id': patch_id,
            'name': patch_name,
            'timestamp': timestamp
        })

        # Write the updated patches to the patches.json file
        with open('patches.json', 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def sort_patches() -> None:
        """
        Sorts the patches by timestamp
        :return: None
        """
        # Open the patches.json file
        with open('patches.json', 'r') as f:
            data = json.load(f)

        # Sort the patches by timestamp
        data['patches'] = sorted(data['patches'], key=lambda x: x['timestamp'])

        # Write the sorted patches to the patches.json file
        with open('patches.json', 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def execute() -> None:
        """
        Executes all patches that have not been executed
        :return: None
        """
        # Open the patches.json file
        with open('patches.json', 'r') as f:
            data = json.load(f)

        # Create the DataHelper
        dh = DataHelper()

        # Loop through the patches
        for patch in data['patches']:
            # Check if the patch has been executed
            if not dh.selectFirstWithParams(
                    'SELECT * FROM installed_patches WHERE patch_id = %s',
                    (f"{patch['id']}_{patch['name']}",)
            ):
                # Print the patch name
                print(f"Executing patch: {patch['id']}_{patch['name']}")

                # Read the patch file
                with open(f'patches/{patch["id"]}_{patch["name"]}.sql', 'r') as f:
                    patch_sql = f.read()

                # Execute the patch line by line
                statements = 0
                for line in patch_sql.split(';'):
                    if len(line) > 0:
                        statements += 1
                        dh.execute(line)

                # Insert the patch into the installed_patches table
                dh.execute(
                    'INSERT INTO installed_patches (patch_id, patch_date) VALUES (%s, %s);',
                    (f"{patch['id']}_{patch['name']}", datetime.utcnow())
                )

                # Print the patch has been executed
                print(f"Executed {statements} statements for patch: {patch['name']}")
            else:
                # Print the patch has already been executed
                print(f"Patch has already been executed: {patch['id']}_{patch['name']}")
