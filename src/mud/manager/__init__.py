import asyncio

from mud.database import Database


class Manager:

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