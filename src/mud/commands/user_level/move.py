#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:33:28 2020

@author: AzureD

First draft of the movement script
"""
from mud.database.datatypes import Location, Coordinates

async def handle(player, database, message: str):
    cmd = message.lower().strip()
    if len(cmd.split(' ')) != 1:
        player.send(f'unrecognized movement command: {message}')

    current_room = await database.world_helper_methods.get_room_document_fields(player.location.world_name,
                                                                                player.location.coordinates.as_dict,
                                                                                'connections')

    if cmd in current_room['connections']:
        # TODO: have a database call for the current room connection instead of player stored
        next_room_coords = current_room['connections'][cmd]
        # TODO: make world name be stored in player
        next_room = await database.world_helper_methods.get_room_document(player.location.world_name,
                                                                          next_room_coords)

        if next_room is None:
            player.send(f"Database ERROR: Cannot find room with id {next_room_coords}")

        else:
            player.move(Location(player.location.world_name,
                                 Coordinates.from_dict(next_room['coordinates'])
                                 )
                        )

            coordinates = next_room['coordinates']
            desc = next_room['description']
            room_exits = next_room['connections']

            player.send(f"You walk off towards '{cmd}' .. or atleast what you percieve as such in the fog\r\n"
                        f"{coordinates}\r\n"
                        f"{desc}\r\n"
                        f"Exits: {room_exits}")

    else:
        player.send('You cannot go that way.')

    return None # to use AWAIT with this and pause command watchdog for players, needs a return


COMMANDS = {'move': handle}