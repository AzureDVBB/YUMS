#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:33:28 2020

@author: AzureD

Move command, moves the player around the connected world and messages people in the locations
they leave/enter.
"""
#type hinting and IDE
from mud.manager import Manager
from mud.database import Database

async def move(database: Database, manager: Manager, player_name: str, message: str):
    """
Moves you, the player, to another location connected to your current one through an exit.

It also will notify the players in the location you leave/enter that you did so.

Usage: move <exit name>

Example: move n
    """

    send_message = ""
    player = manager.player_manager.get_player_data(player_name)

    cmd = message.lower().strip()
    if len(cmd.split(' ')) != 1:
        send_message = f'unrecognized movement command: {message}'
        return None # return early

    current_room = await database.world_helper_methods.get_room_document_fields(player.location,
                                                                                'connections')

    if cmd in current_room['connections']:
        next_room_coords = database.datatypes.Coordinates.from_dict(current_room['connections'][cmd])
        next_room_location = database.datatypes.Location(player.location.world_name, next_room_coords)

        next_room = await database.world_helper_methods.get_room_document(next_room_location)

        if next_room is None:
            send_message = f"Database ERROR: Cannot find room with id {next_room_coords}"

        else:
            # send message to players in room that the player is leaving
            msg = (f"{player_name} walks off towards the '{message}' ... "
                    f"or atleast what is perceptible as such in the fog."
                    )

            players_in_room = manager.player_manager.players_in_location(player.location)
            players_in_room.remove(player_name)
            await manager.connection_manager.send_message_to_many(players_in_room, msg)

            manager.player_manager.move_player(player_name, next_room_location)

            # send message to players in room that the player is entering
            msg = (f"{player_name} walks in from the ever present fog...")

            players_in_room = manager.player_manager.players_in_location(player.location)
            players_in_room.remove(player_name)
            await manager.connection_manager.send_message_to_many(players_in_room, msg)

            # send message to the player
            coordinates = list(next_room['coordinates'].values())
            desc = next_room['description']
            room_exits = list(next_room['connections'].keys())
            players_present = manager.player_manager.players_in_location(player.location)

            send_message = (f"You walk off towards '{cmd}' .. or atleast what you percieve as such in the fog\r\n"
                            f"{coordinates}\r\n"
                            f"Players: {players_present}\r\n"
                            f"{desc}\r\n"
                            f"Exits: {room_exits}"
                            )

    else:
        send_message = 'You cannot go that way.'

    if send_message:
        await manager.connection_manager.send_message(player_name, send_message)
    else:
        await manager.connection_manager.send_message(player_name, "Dunno what happened ERROR")

    return None # to use AWAIT with this and pause command watchdog for players, needs a return


COMMANDS = {'move': move}