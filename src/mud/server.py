#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 08:45:42 2020

@author: AzureDVBB
"""

import asyncio
import socket

from connection import Connection

active_connections = []

async def handle_connection(reader, writer):
    conn = Connection(reader, writer)
    asyncio.ensure_future(conn.read_input(60))
    asyncio.ensure_future(conn.write_output(20))

    active_connections.append(conn) # add to list of active connection

    print(f"Recieved new connection from {conn.address}")
    while conn.is_alive: # periodically check if connection is still active
        await asyncio.sleep(10)

    active_connections.remove(conn) # remove the connection as it closed from the list

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888,
                                        family=socket.AF_INET, flags=socket.AI_PASSIVE,
                                        reuse_address = 1, reuse_port = 1,
                                        ssl=None, ssl_handshake_timeout=None)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

def run():
    asyncio.run(main())