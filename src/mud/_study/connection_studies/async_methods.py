#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 17:01:18 2020

@author: AzureDVBB
"""

import asyncio

class test:

    def __init__(self):

        self.queues = [asyncio.Queue(5)]

    async def put_queues(self, value):
        for q in self.queues:
            # send it off as a task, does not block if a queue is full, but still ensure it recieves it
            asyncio.ensure_future(q.put(value))

    @property
    def take_from_queues(self):
        results = []
        for q in self.queues:
            try:
                r = q.get_nowait()
                results.append(r)
            except asyncio.queues.QueueEmpty:
                continue
        return results

t = test()
asyncio.run(t.put_queues(list(range(3))))
print(t.take_from_queues)