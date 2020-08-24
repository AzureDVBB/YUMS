#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:22:54 2020

@author: AzureD

Instantiation, reference holding to the Interpreter class.

TODO: Make many managers run in processes for load balancing computationally heavy commands.
"""

from mud.commands import Interpreter

# type hinting and IDE
from . import Manager

class InterpreterManager:

    def __init__(self, main_manager: Manager, database_uri: str):
        self.__main_manager = main_manager
        self.__database_uri = database_uri
        self.__interpreter = Interpreter(main_manager, database_uri)


    async def process_input(self, player_name: str, input_message: str):
        await self.__interpreter.process(player_name, input_message)

        return None # needed for async def