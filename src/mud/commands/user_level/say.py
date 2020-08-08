#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 10:19:13 2020

@author: AzureD
"""
# type hint references and IDE help
from mud.player import Player
from mud.database import Database

async def handle(database: Database, manager, player: Player, message: str):

    log_entry = database.datatypes.LogEntry(player.character_name, message)

    await database.world_helper_methods.room_chatlog_add(player.location, 'say', log_entry)

    async for p in manager.world_manager.list_players(player.location):
        p.send(f'{player.character_name} says "{message}" eerily without echoes.')

    return None

COMMANDS = {'say': handle}