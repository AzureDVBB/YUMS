#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:57:26 2020

@author: AzureDVBB

Player class implementation that stores all connections to a single player character.
Implementing functions to read and write to all connections at once.

Also keeps track of player state and location.
"""

import asyncio

# Type hints and IDE help
from mud.connection import Connection

# data structures
from .database.datatypes import Location


class Player:

    # async def to allow awaiting on database fetching
    def __init__(self, database, connection: Connection, character_document,
                 world_manager):

        self.character_name = character_document['name']

        ### connection specific data
        self.__connections = []
        self.command_queue = asyncio.Queue(50)

        # start watching for commands on the first connection
        self.add_connection(connection)

        ### location specific data
        self.__location = Location.from_dict(character_document['location'])

        ### reference to the movement logic from world manager
        self.__world_manager = world_manager


    def __eq__(self, other):
        if not isinstance(other, Player): raise TypeError("Equality operator only supported between player objects.")

        return self.character_name == other.character_name


    async def __command_watch(self, connection: Connection): # watch for command inputs
        while connection.is_alive:
            try: # wrap the read queue into a timeout so it gracefully finishes once connection dies
                command = await asyncio.wait_for(connection.read_queue.get(), 60)
                # put the command from the connection into a shared player queue for the interpreter
                await self.command_queue.put(command)
            except asyncio.TimeoutError:
                # restart while loop to check again if the connection is alive still
                continue
        self.__connections.remove(connection) # ensure connection is removed once it dies

        return None # required return for async function definitions


    @property
    def location(self): # cannot directly set location once initialized, to avoid issues with world manager
        return self.__location

    @property
    def connection_count(self):
        len(self.__connections)

    @property
    def has_connections(self):
        return True if self.__connections else False


    def move(self, new_location: Location): # use the move method to help with moving with the world manager
        self.__world_manager.remove_player(self)
        self.__location = new_location
        self.__world_manager.add_player(self)


    def add_connection(self, connection: Connection):
        self.__connections.append(connection) # add connection to list of active connections
        asyncio.create_task(self.__command_watch(connection)) # watch for command inputs


    def send(self, value: str):
        for conn in self.__connections:
            if conn.is_alive:
                # send the value to all active connections as tasks, so full queues do not block
                asyncio.create_task(conn.write_queue.put(value))
            else:
                self.__connections.remove(conn) # remove dead connections