import sys as __sys
import importlib as __importlib

from mud.text import split

# names of the python modules/packages (folder/file name with no extension)
__all__ = ['user_level']

### Runtime Module Reloading support #############################
##################################################################
__importlib.invalidate_caches()

for __mod in __all__:
    if __mod in dir():
        __importlib.reload(__sys.modules[f"{__name__}.{__mod}"])

del __mod

__importlib.reload(split) # causes it to be reloaded, but also to be loaded twice the first time
##################################################################

from . import * # load all modules with filenames defined by '__all__'

class Interpreter: # interpreter class that holds reference to player/database

    def __init__(self, database): # default values so the examples can work
        self.database = database

    async def process(self, player, message: str):
        command, message = split.command(message)

        if command in user_level.COMMANDS:
            await user_level.COMMANDS[command](player, self.database, message)

        else:
            self.player.send(f"Command not understood: {command}")