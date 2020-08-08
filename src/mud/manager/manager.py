#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:21:04 2020

@author: AzureDVBB
"""

import asyncio

from mud.database import Database
from mud.commands import Interpreter

from .world import World
from .player import PlayerManager
from .authentication import Authentication

class Manager:

    def __init__(self):
        self.world_manager = World()


    def initialize_inside_running_loop(self): # event loop dependant initialization
        # initialize database
        self.database = Database()
        self.__command_interpreter = Interpreter(self.database, self)
        self.__authentication_manager = Authentication(self.database)

        self.player_manager = PlayerManager(self.database, self.__command_interpreter,
                                            self.world_manager, self.__authentication_manager)