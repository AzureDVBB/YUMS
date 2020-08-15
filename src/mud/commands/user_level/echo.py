#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:55:37 2020

@author: AzureDVBB
"""
#type hinting and IDE
from mud.manager import Manager
from mud.database import Database

async def echo(database: Database, manager: Manager, player_name: str, message: str):
    await manager.connection_manager.send_message(player_name, message)

    return None # to use AWAIT with this and pause command watchdog for players, needs a return


# make sure to have the COMMANDS dictionary at the end of the file to house all defined commands
COMMANDS = {'echo': echo}