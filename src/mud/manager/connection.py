#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 17:51:01 2020

@author: AzureD

The management of raw connections, associating them with player names.

Also manages the sending/recieving of messages from all connections associated with players
and calls the command interpreter on recieved messages.
"""

import asyncio

# type hinting and IDE completion
from mud.connection import Connection
from. import Manager


class ConnectionManager:

    def __init__(self, main_manager: Manager):
        self.__main_manager = main_manager # reference to the main manager object

        self.__connected_players = {}


    async def add_connection(self, connection: Connection, character_name: str):
        if not character_name in self.__connected_players:
            self.__connected_players[character_name] = {'connections': [connection,],
                                                        'read_queue': asyncio.Queue(50),
                                                        'write_queue': asyncio.Queue(50)
                                                        }
            # aggregate write_queue distribution logic, run until player disconnects
            asyncio.ensure_future(self.__write_queue_distribution_(character_name))
            # watch for input commands and pass them to the command interpreter
            asyncio.ensure_future(self.__command_watch_(character_name))
            # also add the newly connected player to the PlayerManager
            await self.__main_manager.player_manager.add_player(character_name)

        else:
            self.__connected_players[character_name]['connections'].append(connection)

        # replace old read queue with a new shared one, aggregating user input
        connection.read_queue = self.__connected_players[character_name]['read_queue']

        return None # needed for async def


    async def send_message(self, character_name: list, message: str):
        if character_name in self.__connected_players:
            await self.__connected_players[character_name]['write_queue'].put(message)
        else:
            print("ERROR: ConnectionManager.send_message >>> "
                   f"there is no player connect with character_name '{character_name}'"
                  )

        return None # needed for async def


    async def send_message_to_many(self, character_names: list, message: str):
        for character_name in character_names:
            if character_name in self.__connected_players:
                await self.__connected_players[character_name]['write_queue'].put(message)
            else:
                print("ERROR: ConnectionManager.send_message >>> "
                       f"there is no player connect with character_name '{character_name}'"
                      )

        return None # needed for async def


    async def read_input(self, character_name, message):
        if character_name in self.__connected_players:
            try:
                message = await asyncio.wait_for(self.__connected_players[character_name]['read_queue'].get(), 60)
                return message

            except asyncio.TimeoutError:
                return None
        else:
            print("ERROR: ConnectionManager.send_message >>> "
                  f"there is no player connected with character_name '{character_name}'"
                  )

        return None # needed for async def


    async def __command_watch_(self, character_name: str):
        while character_name in self.__connected_players:
            try:
                message = await asyncio.wait_for(self.__connected_players[character_name]['read_queue'].get(), 60)
            except asyncio.TimeoutError:
                # clear up connections that died
                self.__connected_players[character_name]['connections'] = [conn for conn in
                                                                           self.__connected_players[character_name]['connections']
                                                                           if conn.is_alive
                                                                           ]
                # remove player if no more connections are present for them
                if not self.__connected_players[character_name]['connections']: # no connections associated with player
                    del self.__connected_players[character_name]
                    self.__main_manager.player_manager.remove_player(character_name)
                continue

            await self.__main_manager.interpreter_manager.process_input(character_name, message)

        return None # needed for async def


    async def __write_queue_distribution_(self, character_name: str):
        # while a player character is logged on, listen and send messages down to all connections
        while character_name in self.__connected_players:
            try:
                message = await asyncio.wait_for(self.__connected_players[character_name]['write_queue'].get(), 60)
            except asyncio.TimeoutError:
                continue
            # send message to all active connections for that player
            # use a copy of the list to ensure it runs correctly through each element even as the list is changing
            for conn in self.__connected_players[character_name]['connections']:
                if conn.is_alive: # ensure only connections still alive will be written to else deadlocks can happen
                    await conn.write_queue.put(message)

        return None # needed for async def