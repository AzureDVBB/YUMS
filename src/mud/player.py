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
from .connection import Connection
from .commands import Interpreter

class Player:

    def __init__(self, database, connection: Connection, name: str):

        self.character_name = name
        self.interpreter = Interpreter(self, database)

        ### connection specific data
        self.connections = []
        self.__command_queue = asyncio.Queue(50)
        # start watching for commands and interpret them as they come as a constant coroutine
        self.add_connection(connection)
        asyncio.create_task(self.__interpreter_watch())

        ### location specific data
        # TODO: generalize and initialize based on player that just logged in
        self.location = [2,2]
        self.location_connections = {'w': [1,2], 'e': [3,2], 's': [2,3], 'n': [2,1]}

        # TEMP: add a look command to the command queue to display current spawned room
        self.__command_queue.put_nowait('look')

    async def __command_watch(self, connection: Connection): # watch for command inputs
        while connection.is_alive:
            try: # wrap the read queue into a timeout so it gracefully finishes once connection dies
                command = await asyncio.wait_for(connection.read_queue.get(), 60)
                # put the command from the connection into a shared player queue for the interpreter
                await self.__command_queue.put(command)
            except asyncio.TimeoutError:
                # restart while loop to check again if the connection is alive still
                continue
        self.connections.remove(connection) # ensure connection is removed once it dies

    async def __interpreter_watch(self):
        while len(self.connections) > 0:
            try: # wrap async function into a timeout so it won't wait forever with no connections
                command = await asyncio.wait_for(self.__command_queue.get(), 60)
                await self.interpreter.process(command)
            except asyncio.TimeoutError:
                # restart the while loop to check if player lost all connections (loop can stop)
                continue

    def add_connection(self, connection: Connection):
        self.connections.append(connection) # add connection to list of active connections
        asyncio.create_task(self.__command_watch(connection)) # watch for command inputs

    def send(self, value: str):
        for conn in self.connections:
            if conn.is_alive:
                # send the value to all active connections as tasks, so full queues do not block
                asyncio.create_task(conn.write_queue.put(value))
            else:
                self.connections.remove(conn) # remove dead connections