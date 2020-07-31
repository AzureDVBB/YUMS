#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:14:43 2020

@author: AzureD
"""

async def handle(player, database, message):

    if message == '':
        room = await database.get_room_by_id(player.location)
        if room is None:
            player.send(f"Database ERROR: Room not found {player.location}")
        else:
            room_id = room['room_id']
            desc = room['description']
            exits = list(room['connections'].keys())

            player.send(f"Room ID: {room_id}\r\n"
                        f"{desc}\r\n"
                        f"Exits: {exits}")
    else:
        player.send(f"Command 'look' has no option {message}")

    return None # to use AWAIT with this and pause command watchdog for players, needs a return


COMMANDS = {'look': handle}