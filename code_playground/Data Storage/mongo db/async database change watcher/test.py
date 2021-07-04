#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 16:10:29 2020

@author: AzureD

A test showing how to create a persistent watcher that reacts to database update changes
and only pulls the change.

DISCLAIMER: mongoDB has to be a 'replication set' or 'sharded cluster' for this to work.
"""

import motor.motor_asyncio as motor

import asyncio

import random

from contextlib import suppress


async def create_document(client: motor.AsyncIOMotorClient):
    r = await client['testing_aweasdrta']['log'].insert_many([{'name': "test 1", "log": []},
                                                              {'name': "test 2", "log": []}
                                                              ]
                                                   )

    print(r)
    return None


async def add_log_to_document(db_collection: motor.AsyncIOMotorCollection, docname: str, message: str):
    r = await db_collection.update_one({'name': docname}, # searches for this document to update
                                       {'$push':{ # specifies the operation as 'push'
                                                 'log': { # specifies the awway field to push into
                                                         '$each': [message], # specifies a list of things to push
                                                         '$slice': -7} # specifies that the last 7 elements should be kept
                                                 }
                                        }
                                       )

    # additional notes:
    # SLICE can only be used after an EACH modifier
    # SLICE will take only the last X elements if X is negative, thus suitable for a chatlog
    # UPDATE modifier must be called in order to not overrride the field and for other modifiers to work
    # please follow the template above this text to toy around with
    # see https://docs.mongodb.com/manual/reference/operator/update/slice/#up._S_slice for more info

    print(r)
    return None


async def watch(collection, name: str):

    dockey = await collection.find_one({'name': name}, {'_id': 1}) # get document  key {'_id' : <document id>}

    if not dockey:
        print(f"No document named {name}")
        return None
    else:
        print(f'filtering for document key: {dockey}')

    pipeline = [{'$match': {'operationType': 'update', # filter by operation type
                            'documentKey': dockey, # filter by document key {'_id' : <document id>}
                            'updateDescription.updatedFields.log': {"$exists": True} # filter by field name that changed
                            }
                 },

                {'$addFields': {'log': {'$arrayElemAt': [ # new field called 'log' and put a single array element into
                                                         "$updateDescription.updatedFields.log", # $ expression pointing to the array field
                                                         -1 # the element index (-1 means the last element)
                                                         ]
                                        } # copy embedded log field to top level 'log'
                                }
                 },

                {'$project': {'log': 1, # only bring back log field
                              }
                  },# NOTE: for some reason if you filter out '_id' field this way everything breaks

                ]


    # example straight from https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html


    # for some reason this always prints the result object ....
    async with collection.watch(pipeline=pipeline, batch_size=1) as change_stream: # async context manager, allowing safe closing of stream

        async for change in change_stream: # async for loop yielding results and awaiting for more from an async generator
            print(change) # the main logic goes here, please no 'return' in here, use 'yield' if you must, but a better way is using queues

    return None # add a return value as is required by the async def


async def run():
    client = motor.AsyncIOMotorClient("mongodb://localhost:27017")

    # Uncomment these two lines whenever on a new database

    # await client.drop_database('testing')
    # await create_document(client)

    watcher_task = asyncio.ensure_future(watch(client['testing_aweasdrta']['log'], 'test 1')) # start watching for updates
    await asyncio.sleep(1)
    await add_log_to_document(client['testing_aweasdrta']['log'], 'test 1', f'test! {random.randint(0, 100)}')
    await asyncio.sleep(4)
    await add_log_to_document(client['testing_aweasdrta']['log'], 'test 2', f'test! {random.randint(0, 100)}')
    await asyncio.sleep(4)
    await add_log_to_document(client['testing_aweasdrta']['log'], 'test 1', f'test! {random.randint(0, 100)}')
    await asyncio.sleep(20)
    watcher_task.cancel() # stop watching for updates
    return None

asyncio.run(run())