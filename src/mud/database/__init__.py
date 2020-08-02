"""

"""

import sys as __sys
import importlib as __importlib

import motor.motor_asyncio
import asyncio

# names of the python modules/packages (folder/file name with no extension)
__all__ = ['character', 'world']

### Runtime Module Reloading support #############################
##################################################################
__importlib.invalidate_caches()

for __mod in __all__:
    if __mod in dir():
        __importlib.reload(__sys.modules[f"{__name__}.{__mod}"])

del __mod
##################################################################

from . import * # load all modules with filenames defined by '__all__'

class Database:

    __user_database_name = "test-users" # the database name where all user data is stored
    __character_collection_name = "test-characters" # collection where individual characters and login is stored
    __account_collection_name = "test-accounts" # collection where individual player accounts are stored

    __world_database_name = "test-world" # the database name where all world data is kept
    __tutorial_collection_name = "tutorial" # the name of the collection where the tutorial is stored

    def __init__(self, database_uri='mongodb://localhost:27017'):
        """
        Initialize the asynchronous client for the database inside the running eventloop.
        Due to the import happening before the event loop being established
        this init function must be called from the main server function to ensure
        the correct and running event loop is being passed on.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(database_uri,
                                                             io_loop=asyncio.get_running_loop()
                                                             )
        self.character = character.Character(self.client[self.__user_database_name][self.__character_collection_name])
        self.world = world.World(self.client[self.__world_database_name])