#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:33:28 2020

@author: AzureD

First draft of the movement script
"""
# type hint references and IDE help
from mud.player import Player
from mud.database import Database

async def handle(database: Database, manager, player: Player, message: str):
    cmd = message.lower().strip()
    if len(cmd.split(' ')) != 1:
        player.send(f'unrecognized movement command: {message}')

    current_room = await database.world_helper_methods.get_room_document_fields(player.location,
                                                                                'connections')

    if cmd in current_room['connections']:
        next_room_coords = database.datatypes.Coordinates.from_dict(current_room['connections'][cmd])
        next_room_location = database.datatypes.Location(player.location.world_name, next_room_coords)

        next_room = await database.world_helper_methods.get_room_document(next_room_location)

        if next_room is None:
            player.send(f"Database ERROR: Cannot find room with id {next_room_coords}")

        else:
            for p in manager.world_manager.list_players(player.location):
                if p == player: # skip the player moving from recieving the move message
                    continue
                p.send(f"{player.character_name} walks off towards the '{message}' ... "
                       f"or atleast what is perceptible as such in the fog.")

            player.move(next_room_location)

            for p in manager.world_manager.list_players(player.location):
                if p == player: # skip the player moving from recieving the move message
                    continue
                p.send(f"{player.character_name} walks in from the '{message}' ... "
                       f"or atleast what is perceptible as such in the fog.")

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