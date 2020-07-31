# NOTE: this is copy pasted of the top 'user_level' package '__init__.py' script esentially
# so please use those in subpackages as well

import sys as __sys
import importlib as __importlib

# Only add the names of the modules that have the COMMANDS dictionary definition
# that is, they define the commands, as there can be helper modules for complex ones
__all__ = ['example3', 'example4']

### Runtime Module Reloading support #############################
############## see 'commands/__init__.py' for more comments ######

for __mod in __all__:
    if __mod in dir():
        __importlib.reload(__sys.modules[f"{__name__}.{__mod}"])

del __mod
##################################################################

from . import *

COMMANDS = {} # aggregate the package module's COMMANDS dictionaries

### Collect Implemented Command References #######################
######## from all loaded modules stored in <module>.COMMAND ######

for __mod in __all__: # loop through all module names defined in __all__
    if __mod in dir(): # check if module name is loaded

        __cmd = __sys.modules[f"{__name__}.{__mod}"].COMMANDS # get the COMMAND dictionary from module

        for __key in __cmd.keys(): # check each dictionary key for COMMAND

            if not (__key in COMMANDS): # Add the COMMAND key/reference pair if not allready added

                # make a new dictionary out of key/reference and add that to the COMMANDS master dict
                # This is actually neccessary to facilitate key-by-key checking and updating
                # so even if one package/module that defines more then one command has a conflict
                # the rest of those defined COMMANDS will be entered into the master dictionary
                COMMANDS.update({__key: __cmd[__key]})

            else: # print and ignore any duplicate commands people have created
                print(f"ERROR Duplicate command found ignoring... : {__key}")

del __mod, __cmd, __key
##################################################################