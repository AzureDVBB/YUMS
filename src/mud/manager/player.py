#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:14:21 2020

@author: AzureD
"""

import asyncio

# type hinting and IDE
from mud.database import Database
from mud.connection import Connection
from mud.player import Player

class PlayerManager:

    def __init__(self, database_ref: Database, interpreter_ref,
                 world_manager_ref, authentication_manager_ref):

        self.new_connections = []
        self.active_players = {}

        self.__database = database_ref
        self.__interpreter = interpreter_ref
        self.__world_manager = world_manager_ref
        self.__authentication = authentication_manager_ref


    async def new_connection(self, connection: Connection):
        self.new_connections.append(connection)
        await connection.write_queue.put(f"Welcome to the in-development mud game!"
                                         f"please enjoy your stay. \r\n"
                                         f"You can log in by typing: \r\n"
                                         f"login <name> <password>\r\n"
                                         f"Or register by typing:\r\n"
                                         f"register <name> <password>\r\n"
                                         f"Note that names should be lower case and cannot contain"
                                         f"spaces, passwords cannot contain spaces.")

        character_document = await self.__authentication.authenticate_connection(connection)
        if character_document: # document is not none
            self.add_player(connection, character_document)

        return None # async spec


    async def __watch_commands(self, player: Player):
        while player.has_connections: # while there are still connections on player
            try: # wait for and interpret aggregate commands
                command = await asyncio.wait_for(player.command_queue.get(), 30)
                await self.__interpreter.process(player, command)
            except asyncio.TimeoutError: # continue after a few seconds to check if player still conencted
                continue

        self.__world_manager.remove_player_from_world(player) # remove player from the world manager
        del self.active_players[player.character_name] # delete player reference
        print(f"player {player.character_name} disconnected")

        return None # async spec, has to have a return in there


    def add_player(self, connection: Connection, character_document):
        name = character_document['name']

        if name in self.active_players:
            self.active_players[name].add_connection(connection)

        else:
            # create and add players to the master player list, passing movement logic to them
            self.active_players[name] = Player(self.__database, connection, character_document,
                                               self.__world_manager)

            # add them to the world manager
            self.__world_manager.add_player(self.active_players[name])

            #begin watching for aggregate commands while they are connected
            asyncio.ensure_future(self.__watch_commands(self.active_players[name]))