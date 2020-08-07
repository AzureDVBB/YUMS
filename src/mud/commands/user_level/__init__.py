import sys as __sys
import importlib as __importlib

# names of the python packages/modules (folder/file names with no extension)
__all__ = ['look', 'echo', 'move', 'say']

### Runtime Module Reloading support #############################
############## see 'commands/__init__.py' for more comments ######

for __mod in __all__:
    if __mod in dir():
        __importlib.reload(__sys.modules[f"{__name__}.{__mod}"])

del __mod
##################################################################

from . import *

COMMANDS = {}

### Collect Implemented Command References #######################
######## from all loaded modules stored in <module>.COMMAND ######

for __mod in __all__:
    if __mod in dir():

        __cmd = __sys.modules[f"{__name__}.{__mod}"].COMMANDS

        for __key in __cmd.keys():
            if not (__key in COMMANDS):

                COMMANDS.update({__key: __cmd[__key]})

            else: # print and ignore any duplicate commands people have created
                print(f"ERROR Duplicate command found ignoring... : {__key}")


del __mod, __cmd, __key
##################################################################