import sys as __sys
import importlib as __importlib

from mud.text import split
from mud.database import Database

# type hinting and IDE
from mud.manager import Manager

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

    def __init__(self, manager: Manager, database_uri: str): # default values so the examples can work
        self.database = Database(database_uri)
        self.manager = manager

    async def process(self, player_name: str, message: str):
        command, message = split.command(message)

        if command in user_level.COMMANDS:
            await user_level.COMMANDS[command](self.database, self.manager, player_name, message)

        else:
            await self.manager.connection_manager.send_message(player_name, f"Command not understood: {command}")

        return None # needed for async definition