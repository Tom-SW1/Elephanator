import json
import sys
import os

from Logic.PatchesSignature import PatchesSignature
from Logic.Commands.Patch import Patch

# Configuration checks start here

# Ensure patches.json and patches folder exist, if not, create them
if not os.path.exists('patches'):
    os.makedirs('patches')

if not os.path.exists('patches.json'):
    with open('patches.json', 'w') as f:
        f.write('{"patches": []}')

# If the patches.signature file does not exist then create it, and assign a stamp and signature
if not os.path.exists('patches.signature.json'):
    PatchesSignature.updateSignature()

# Retrieve appsettings.json and set environment variables
if os.path.exists('appsettings.json'):
    with open('appsettings.json', 'r') as f:
        appsettings = json.load(f)
        for key in appsettings:
            os.environ[key] = appsettings[key]

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

print(data)
if data['operation'] == 'addpatch':
    Patch.add(data)