#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:14:43 2020

@author: AzureD
"""
#type hinting and IDE
from mud.manager import Manager
from mud.database import Database

async def look(database: Database, manager: Manager, player_name: str, message: str):
    player_location = manager.player_manager.player_data[player_name].location

    send_message = ''

    if message == '':
        # TODO: make world, name also a player, thingy
        room = await database.world_helper_methods.get_room_document(player_location)

        if room is None:
            send_message = f"Database ERROR: Room not found {player_location}"
        else:
            coordinates = list(room['coordinates'].values())
            desc = room['description']
            exits = list(room['connections'].keys())
            players_present = manager.player_manager.players_in_location(player_location)

            send_message = (f"Room coordinates: {coordinates}\r\n"
                            f"Players: {players_present}\r\n"
                            f"{desc}\r\n"
                            f"Exits: {exits}"
                            )
    else:
        send_message = f"Command 'look' has no option {message}"

    await manager.connection_manager.send_message(player_name, send_message)

    return None # needed for async def


COMMANDS = {'look': look}