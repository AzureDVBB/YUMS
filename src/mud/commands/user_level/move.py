#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:33:28 2020

@author: AzureD

First draft of the movement script
"""

async def handle(player, database, message: str):
    cmd = message.lower().strip()
    if len(cmd.split(' ')) != 1:
        player.send(f'unrecognized movement command: {message}')

    elif cmd in player.location_connections:
        next_room_id = player.location_connections[cmd]
        next_room = await database.get_room_by_id(next_room_id)

        if next_room is None:
            player.send(f"Database ERROR: Cannot find room with id {next_room_id}")

        else:
            player.location = next_room['room_id']
            player.location_connections = next_room['connections']

            room_id = next_room['room_id']
            desc = next_room['description']
            room_exits = list(next_room['connections'].keys())

            player.send(f"You walk off towards '{cmd}' .. or atleast what you percieve as such in the fog\r\n"
                        f"{room_id}\r\n"
                        f"{desc}\r\n"
                        f"Exits: {room_exits}")

    else:
        player.send('You cannot go that way.')

    return None # to use AWAIT with this and pause command watchdog for players, needs a return


COMMANDS = {'move': handle}