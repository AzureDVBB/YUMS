#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 19:08:40 2020

@author: AzureDVBB

An echo server for MUD clients that handles disconnections and timeouts gracefully.
"""

import asyncio

async def handle_connection(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"!!!! New connection recived from: {addr}")
    while True:
        data = await reader.read(100)
        if data == b'':
            break
        message = data.decode()
        print(f">>>> Recieved message '{message.strip()}'")
        print("<<<< Echoing back..")
        writer.write(data)
        await writer.drain()
    print(f"XXXX Closing connection from {addr}")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())