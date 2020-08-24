import asyncio

from mud.database import Database


class Manager:
    """
    The manager package responsible for the management of players and complex systems inside the MUD.

    Anything that has several states, affect players or rooms, pretty much happens here at runtime.

    Do note: It needs initialization inside the running loop (due to many modules depending on it),
    as such, a special (totally not __init__) method has been created. Why? See 'src/mud/server.py'

    As a bonus, doing import inside the special init method allows this Manager class to be imported
    by all modules, including those that are imported into it, for type hinting and IDE stuff by
    avoiding circular import errors.
    """

    def __init__(self):
        pass


    def initialize_inside_running_loop(self): # event loop dependant initialization
        # initialize database
        self.database = Database()
        # initialize managers that hold references to the main manager
        # bury import statements for them in initilization to avoid circular import errors
        from .authentication import AuthenticationManager
        from .interpreter import InterpreterManager
        from .connection import ConnectionManager
        from .player import PlayerManager

        self.authentication_manager = AuthenticationManager(self, self.database.uri)
        self.player_manager = PlayerManager(self, self.database.uri)
        self.connection_manager = ConnectionManager(self)
        self.interpreter_manager = InterpreterManager(self, self.database.uri)