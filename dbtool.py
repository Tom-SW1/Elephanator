import sys
import json
import os

from Logic.PatchesSignature import PatchesSignature
from Logic.Commands.Patch import Patch
from Logic.Commands.Init import Init
from Logic.Commands.Execute import Execute

# Configuration checks start here

# Ensure patches.json and patches folder exist, if not, create them
if not os.path.exists('patches'):
    os.makedirs('patches')

if not os.path.exists('patches.json'):
    with open('patches.json', 'w') as f:
        f.write('{"patches": []}')

# Ensure there is an appsettings.json file
if not os.path.exists('appsettings.json'):
    with open('appsettings.json', 'w') as f:
        f.write('{"connectionString": null}')

# Check the appsettings.json to ensure it has a connectionString, then prompt the user to enter one
with open('appsettings.json', 'r') as f:
    data = json.load(f)
    if data['connectionString'] is None:
        # Prompt the user to enter the connection string
        print("Required format: 'host=***;port=5432;dbname=***;user=***;password=***;'")
        print('Please enter the connection string for the database:')
        data['connectionString'] = input()

        # Write the connection string to the appsettings.json file
        with open('appsettings.json', 'w') as f:
            f.write(f'{{"connectionString": "{data["connectionString"]}"}}')

    # Add the connection string to the environment variables
    os.environ['connectionString'] = data['connectionString']

# Ensure each patch directory has a test folder TODO: Implement unit tests
for patch in os.listdir('patches'):
    if not os.path.exists(f'patches/{patch}/test'):
        os.makedirs(f'patches/{patch}/test')

# If the patches.signature file does not exist then create it, and assign a stamp and signature
if not os.path.exists('patches.signature.json'):
    PatchesSignature.updateSignature()

# Check if the signature of patches.json has changed due to a git pull
if PatchesSignature.hasDifferentSignature():
    # If it has changed, so ensure the patches are sorted by timestamp and the signature is updated
    PatchesSignature.updateSignatureWithSort()

# Command processing starts here

# Get command line arguments
args = sys.argv

# Map the operation and arguments onto a dictionary
data = {
    'operation': None,
    'arguments': {}
}

lastKey = None
for i in range(1, len(args)):
    try:
        # If the file ends with .py then ignore it
        if args[i].endswith('.py'):
            continue
        else:
            # If the operation is None then set it to the current argument
            if data['operation'] is None:
                data['operation'] = args[i].strip('-').lower()
            # Otherwise process it as an argument
            else:
                # If the value starts with -- then it is a key, so add it to the dictionary
                if args[i].startswith('--'):
                    lastKey = args[i].strip('-').lower()
                    data['arguments'][lastKey] = []
                # Otherwise, add the value to the last key
                else:
                    data['arguments'][lastKey].append(args[i])
    except:
        raise Exception('Invalid arguments: Arguments must be in the form of --key value')

# Route the operation to the appropriate function

if data['operation'] == 'addpatch':
    Patch.add(data)
elif data['operation'] == 'init':
    Init.execute(data)
elif data['operation'] == 'execute':
    Execute.run(data)
# Throw an error if the operation is not recognised
else:
    raise Exception('Invalid operation: Must be addpatch, init or execute')