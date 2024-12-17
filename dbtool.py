import sys
import os

from Logic.Initialisation import Initialisation
from Logic.Patches import Patches

# Print help message
def print_help():
    """
    Prints the help message
    :return: None
    """
    print("""Invalid arguments!
    Commands:
        python dbtool.py --init --connectionstring "<connection string>" => Initialise the database with a connection string
        python dbtool.py --addpatch --name <patch name> => Add a database patch
        python dbtool.py --execute => Execute the database patches
            """)

# Get command line arguments
args = sys.argv

# Install Pip dependencies through the requirements.txt file
os.system('pip install -r requirements.txt')

# Check if the command is an initialisation command
if len(args) == 4:
    if args[1] == '--init':
        # Check if the command is an initialisation command with a connection string
        if args[2] == '--connectionstring':
            # Run the connection string initialisation
            Initialisation.connection_string(args[3])

# Run the initialisation checks
init_error = False
try:
    Initialisation.execute()
except Exception as e:
    init_error = True
    print(e)

if not init_error:
    # Add patch command
    if len(args) >= 4:
        if args[1] == '--addpatch' and args[2] == '--name':
            Patches.create_patch(' '.join(args[3:]))
        else:
            print_help()
    # Execute command
    elif len(args) >= 2:
        if args[1] == '--execute':
            Patches.execute()
        # Ignore --init commands
        elif args[1] == '--init':
            pass
        else:
            print_help()
    else:
        print_help()
