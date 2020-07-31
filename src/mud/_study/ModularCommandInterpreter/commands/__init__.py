# using the 'as' keyword to alias it as a double underscore leading name not only aliases
# it but also hides it from my IDE's search bar so its alot cleaner, hah!
import sys as __sys
import importlib as __importlib

# names of the python modules/packages (folder/file name with no extension)
__all__ = ['user_level', 'admin_level']


### Runtime Module Reloading support #############################
##################################################################

# invalidate import caches (paths, files, etc.) to avoid potential bugs for more info on it see
# http://ballingt.com/import-invalidate-caches/
# it is (hopefully) enough to call this at the top level '__init__.py' file, is my assumption
__importlib.invalidate_caches()

for __mod in __all__: # go through each module name

    if __mod in dir(): # check if module is allready loaded in THE LOCAL SCOPE

        # 'sys.modules' is a dictionary containing all loaded module names mapped to their reference
        # the names defined in 'sys.modules' store the absolute path to each module
        # so to reference the package we need the <absolute path>.<module name> format
        __importlib.reload(__sys.modules[f"{__name__}.{__mod}"]) # reload module by name in THE LOCAL SCOPE

del __mod # clean up the now unneded variable, it was also made not to show up in IDE with __name
##################################################################

from . import * # load all modules with filenames defined by '__all__'

class Interpreter: # interpreter class that holds reference to player/database

    def __init__(self, player=None, database=None): # default values so the examples can work
        self.player = player
        self.database = database

    def process(self, command: str, message: str):
        if command in user_level.COMMANDS:
            user_level.COMMANDS[command](self.player, self.database, message)
        elif command in admin_level.COMMANDS:
            admin_level.COMMANDS[command](self.player, self.database, message)
        else:
            print(f"Command was not understood: {command}")