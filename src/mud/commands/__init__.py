import sys as __sys
import importlib as __importlib

from . import helper_functions

# names of the python modules/packages (folder/file name with no extension)
__all__ = ['user_level']

### Runtime Module Reloading support #############################
##################################################################
__importlib.invalidate_caches()

for __mod in __all__:
    if __mod in dir():
        __importlib.reload(__sys.modules[f"{__name__}.{__mod}"])

del __mod

__importlib.reload(helper_functions)
##################################################################

from . import * # load all modules with filenames defined by '__all__'

class Interpreter: # interpreter class that holds reference to player/database

    def __init__(self, player, database): # default values so the examples can work
        self.player = player
        self.database = database

    async def process(self, message: str):
        command, message = helper_functions.separate_prefix(message)
        if command in user_level.COMMANDS:
            await user_level.COMMANDS[command](self.player, self.database, message)

        else:
            self.player.send(f"Command not understood: {command}")