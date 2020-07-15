#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:04:34 2020

@author: AzureDVBB
Experimenting to see if reader/writer could be separated to perform them concurrently.
"""

import asyncio
import socket

import telnet

class Connection:
    # TODO: Optimize with __slots__
    # TODO: Test extensively

    def __init__(self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter):
        self.reader = reader
        self.writer = writer

        self.address = writer.get_extra_info('peername')

        self.reader_queue = asyncio.Queue(50) # WARNING: this queue full might be problematic, blocks
        self.writer_queue = asyncio.Queue(50) # same here

        self.is_alive = True
        self.timed_out = False

        self.reader_coroutine_closed = False
        self.writer_coroutine_closed = False


async def read_input(connection, timeout: int=None):
    assert timeout > 1 or timeout is None, "timeout should not be less then 1, only None"

    print(f"READER Starting to serve read requests for {connection.address}")
    while connection.is_alive: # support remotely killing connections by a single value
        if connection.is_alive == False:
            print(f"WRITER Connection closed from {connection.address}")
            break
        # print(f"READER inside loop")
        try:
            # read 100 bytes of data and analyse it, recieving TELNET commands do not have
            # a newline at the end so readline() cannot be used here
            result = await asyncio.wait_for(connection.reader.read(200), timeout=timeout)
            connection.timed_out = False # reset this on every recieved message
            print(f"READER: Recieved message {result} from {connection.address}")
            if result == b'': # connection closed prematurely
                print(f"READER Disconnected from {connection.address}")
                connection.is_alive = False
                break

            if not result[0] == telnet.Code.IAC: # check to see if its not a TELNET command
                if not result.endswith(b'\r\n'):
                    result += await asyncio.wait_for(connection.reader.readline(), timeout=timeout)
                await connection.reader_queue.put(result) # block here if command processor overload

        # client took too long to send new commands, check if they are still connected
        except asyncio.TimeoutError:
            print(f"READER {connection.address} timed out")
            if not connection.timed_out:
                print(f"READER sending are-you-there ping on {connection.address}")
                connection.timed_out = True
                # FIXME: the telnet AYT command is not guaranteed to be supported and is not guaranteed to return
                # TINTIN++ returns once with IAC DONT AYT and then never returns again
                # MUDLET returns always with IAC WONT AYT with every ping
                await connection.writer_queue.put(bytes([255, 253, 246]))
                                                  # 'keepalive ****\r\n'.encode())
            else:
                print(f"READER 2nd commection timeout in a row, disconnecting {connection.address}")
                connection.is_alive = False

    # teardown
    connection.reader_coroutine_closed = True


async def write_output(connection, timeout: int=2):
    assert timeout > 1, "sleep should not be less then 1, only None"

    print(f"WRITER Starting to serve write requests for {connection.address}")
    while connection.is_alive:
        # print(f"WRITER inside loop")
        try:
            msg = await asyncio.wait_for(connection.writer_queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            continue
        print(f"WRITER Recieved new message to write: {msg}")
        connection.writer.write(msg)

        print(f"WRITER Draining writer for {connection.address}")
        await connection.writer.drain()

    # teardown logic
    connection.writer.close()
    connection.writer_coroutine_closed = True
    connection.is_alive = False

#####################################################################################

active_connections = []

async def echo(conn):
    while conn.is_alive:
        read = await conn.reader_queue.get()
        print(f"ECHO returning {read.strip()}")
        await conn.writer_queue.put(read)

async def handle_connection(reader, writer):
    conn = Connection(reader, writer)
    asyncio.ensure_future(read_input(conn, 20))
    asyncio.ensure_future(write_output(conn, 2))
    asyncio.ensure_future(echo(conn))

    active_connections.append(conn)

    print(f"Recieved new connection from {conn.address}")
    while conn.is_alive:
        await asyncio.sleep(10)
    # teardown, so the active connections is updated
    active_connections.remove(conn)


async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888,
                                        family=socket.AF_INET, flags=socket.AI_PASSIVE,
                                        reuse_address = 1, reuse_port = 1,
                                        ssl=None, ssl_handshake_timeout=None)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
