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

class Player:

    def __init__(self, connection):

        self.connections = [connection]

        self.character = None


    def write(self, value):
        for conn in self.connections:
            if conn.is_alive:
                # send the value to all active connections as tasks, so full queues do not block
                asyncio.ensure_future(conn.writer_queue.put(value))
            else:
                self.connections.remove(conn) # remove dead connections

    def read(self):
        results=[]
        for conn in self.connections:
            if conn.is_alive:
                try:
                    results.append(conn.reader_queue.get_nowait()) # do not block on empty queues

                except asyncio.QueueEmpty:
                    continue

            else:
                self.connections.remove(conn) # remove dead connections

        return results