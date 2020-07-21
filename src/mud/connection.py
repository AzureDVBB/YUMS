#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 08:45:59 2020

@author: AzureDVBB
"""

import asyncio

class Connection:
    # TODO: ensure slots are up do date when changing things
    __slots__ = ['reader', 'writer', 'address', 'read_queue', 'write_queue',
                 'is_alive', 'reader_coroutine_closed', 'writer_coroutine_closed']
    # TODO: Test extensively

    def __init__(self, reader: asyncio.streams.StreamReader,
                 writer: asyncio.streams.StreamWriter):
        self.reader = reader
        self.writer = writer

        self.address = writer.get_extra_info('peername')

        self.read_queue = asyncio.Queue(50) # WARNING: this queue full might be problematic, blocks
        self.write_queue = asyncio.Queue(50) # same here

        self.is_alive = True

        self.reader_coroutine_closed = False
        self.writer_coroutine_closed = False

        asyncio.ensure_future(self.__read_input())
        asyncio.ensure_future(self.__write_output())


    async def __read_input(self, timeout: int=60):
        assert timeout >= 10, "timeout should not be less then 10s"

        while self.is_alive: # support remotely killing connections by a single value
            try:
                result = await asyncio.wait_for(self.reader.readline(), timeout=timeout)

                if result == b'': # connection closed prematurely
                    self.is_alive = False
                    break

                # block here if command processor overload
                await self.read_queue.put(result.decode('ascii'))

            # client took too long to send new commands, check if connection got terminated
            except asyncio.TimeoutError:
                continue # restart loop to check if connection is alive

        self.reader_coroutine_closed = True # teardown logic


    async def __write_output(self, timeout: int=20):
        assert timeout >= 10, "timeout should not be less then 10s"

        while self.is_alive:
            try:
                msg = await asyncio.wait_for(self.write_queue.get(), timeout=timeout)

            # no new messages to write for too long, check if connection is still alive
            except asyncio.TimeoutError:
                continue # restart loop to check if connection is alive

            self.writer.write(msg.encode('ascii') + b'\r\n')
            await self.writer.drain()

        # teardown logic
        self.writer.close()
        self.writer_coroutine_closed = True
        self.is_alive = False