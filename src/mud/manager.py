#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:21:04 2020

@author: AzureDVBB
"""

from .player import Player
from .connection import Connection
from .command_interpreter import interpret

class Manager:
    active_players = {}
    new_connections = []

    async def add_connection(self, connection: Connection):
        self.new_connections.append(connection)
        await connection.write_queue.put("Welcome to the in-development mud game!" +
                                         "please enjoy your stay. \r\n" +
                                         "You can log in by typing: \r\n" +
                                         "login guest <name>")
        while True:
            cmd = await connection.read_queue.get()
            result, message = interpret(cmd)
            if not (result is False):
                await self.add_player(connection, result)
                await connection.write_queue.put(message)
                break
            else:
                await connection.write_queue.put(message)

        self.new_connections.remove(connection)


    async def add_player(self, connection: Connection, name: str):
        if name in self.active_players:
            self.active_players[name].add_connection(connection)
        else:
            self.active_players[name] = Player(connection, name)
