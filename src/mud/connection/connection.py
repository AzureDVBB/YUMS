#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 08:45:59 2020

@author: AzureDVBB
"""

import asyncio


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

        self.reader_coroutine_closed = False
        self.writer_coroutine_closed = False


async def read_input(connection, timeout: int=None):
    assert timeout > 1 or timeout is None, "timeout should not be less then 1, only None"

    while connection.is_alive: # support remotely killing connections by a single value
        try:
            result = await asyncio.wait_for(connection.reader.readline(), timeout=timeout)

            if result == b'': # connection closed prematurely
                connection.is_alive = False
                break

            await connection.reader_queue.put(result) # block here if command processor overload

        # client took too long to send new commands, check if connection got terminated
        except asyncio.TimeoutError:
            continue # restart loop to check if connection is alive

    connection.reader_coroutine_closed = True # teardown logic


async def write_output(connection, timeout: int=2):
    assert timeout > 1, "sleep should not be less then 1, only None"

    while connection.is_alive:
        try:
            msg = await asyncio.wait_for(connection.writer_queue.get(), timeout=timeout)

        # no new messages to write for too long, check if connection is still alive
        except asyncio.TimeoutError:
            continue # restart loop to check if connection is alive

        connection.writer.write(msg)
        await connection.writer.drain()

    # teardown logic
    connection.writer.close()
    connection.writer_coroutine_closed = True
    connection.is_alive = False