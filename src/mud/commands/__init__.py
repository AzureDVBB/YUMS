"""
The modular, Reloadable command interpreter.

This package implements logic for dynamically Loading/Reloading logic, use 'importlib.reload()' .

The main class it implements is 'Interpreter' which has a single method 'process' to deal with
player commands.

Subpackages and modules that implement the actual logic are listed in '__all__' and thus need
to be updated whenever a new one is created in order to be loaded and used, as a bonus, to see
this change during runtime simply reload this module and re-instantiate the 'Interpreter' class.
"""

import sys as __sys
import importlib as __importlib

from mud.text import split
from mud.text.help_format import docstring_to_help
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
    """
    Class holding references to the manager and database to be used with its only method: 'process'
    which holds the switching logic to the player commands.
    """

    def __init__(self, manager: Manager, database_uri: str): # default values so the examples can work
        """
        Create database connection and save reference to the manager.
        """
        self.database = Database(database_uri)
        self.manager = manager

    async def process(self, player_name: str, message: str):
        """
        Method that takes in a message and tries to interpret it as a command.

        It seperates off the first word of the message, searches if that is an actual command
        and calls it's associated function to handle the command, with the remainder of the message.

        Parameters
        ----------
        player_name : str
            Name of the player sending the message.
        message : str
            Message from a player to be interpreted as a command.

        Returns
        -------
        None
            Return just needed for the async definition.

        """
        command, message = split.command(message)

        if command in user_level.COMMANDS:

            # display the #help for the command if called for it with: <command> #help
            if message.startswith("#help"):
                docstring = user_level.COMMANDS[command].__doc__
                help_message = docstring_to_help(command, docstring)
                await self.manager.connection_manager.send_message(player_name, help_message)

            # call the command handling function
            else:
                await user_level.COMMANDS[command](self.database, self.manager, player_name, message)

        else:
            await self.manager.connection_manager.send_message(player_name, f"Command not understood: {command}")

        return None # needed for async definition