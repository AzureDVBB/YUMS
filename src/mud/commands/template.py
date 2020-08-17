#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on <DateHere>

@author: <name>
"""
#type hinting and IDE
from mud.manager import Manager
from mud.database import Database

async def command_handler(database: Database, manager: Manager, player_name: str, message: str):
    """
This is the help of the command.

Usage: how to use it

Example: concrete example using it
    """

    pass # python logic goes here

    return None

COMMANDS = {'command_name': command_handler}