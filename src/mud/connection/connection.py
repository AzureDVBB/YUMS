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


    async def read_input(self, timeout: int=60):
        assert timeout >= 10, "timeout should not be less then 10s"

        while self.is_alive: # support remotely killing connections by a single value
            try:
                result = await asyncio.wait_for(self.reader.readline(), timeout=timeout)

                if result == b'': # connection closed prematurely
                    self.is_alive = False
                    break

                # block here if command processor overload
                await self.reader_queue.put(result.decode('ascii'))

            # client took too long to send new commands, check if connection got terminated
            except asyncio.TimeoutError:
                continue # restart loop to check if connection is alive

        self.reader_coroutine_closed = True # teardown logic


    async def write_output(self, timeout: int=20):
        assert timeout >= 10, "timeout should not be less then 10s"

        while self.is_alive:
            try:
                msg = await asyncio.wait_for(self.writer_queue.get(), timeout=timeout)

            # no new messages to write for too long, check if connection is still alive
            except asyncio.TimeoutError:
                continue # restart loop to check if connection is alive

            self.writer.write(msg.encode('ascii') + b'\r\n')
            await self.writer.drain()

        # teardown logic
        self.writer.close()
        self.writer_coroutine_closed = True
        self.is_alive = False