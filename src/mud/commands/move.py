#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:33:28 2020

@author: AzureD

First draft of the movement script
"""
import pymongo # TODO: change blocking pymongo library to motor (asyncio)

tutorial_map = pymongo.MongoClient('mongodb://localhost:27017')['test-world']['tutorial']

def handle(message: str, player):
    cmd = message.lower().strip()
    if len(cmd.split(' ')) != 1:
        return (False, f'unrecognized movement command: {message}')

    elif cmd in player.location_connections:
        next_room_id = player.location_connections[cmd]
        next_room = tutorial_map.find_one({'room_id': next_room_id})

        if next_room is None:
            return (False, f"Database ERROR: Cannot find room with id {next_room_id}")

        player.location = next_room['room_id']
        player.location_connections = next_room['connections']

        room_id = next_room['room_id']
        desc = next_room['description']
        room_exits = list(next_room['connections'].keys())

        return (True, f"You walk off towards '{cmd}' .. or atleast what you percieve as such in the fog\r\n"
                f"{room_id}\r\n"
                f"{desc}\r\n"
                f"Exits: {room_exits}")

    else:
        return(False, 'You cannot go that way.')

IMPLEMENTED = {'move': handle}