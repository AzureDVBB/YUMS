#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:57:35 2020

@author: AzureD
"""

import asyncio

class World:

    def __init__(self, database):
        self.database = database


    async def get_room_document_fields(self, world_name: str, coordinates, field_names: list):
        whitelisted_fields = {field: 1 for field in field_names} # works like a list comprehension

        document = await self.database[world_name].find_one( # world_name collection in the database
                                                            {'coordinates': coordinates}, # get room by id
                                                            {'_id': 0, # do not get the document id
                                                             }.update(whitelisted_fields) # add whitelist
                                                            )

        # return None if document does not exist or document has no field with name: field_name
        return document if document else None


    async def get_room_document(self, world_name: str, coordinates: list):
        document = await self.database[world_name].find_one({'coordinates': coordinates},
                                                            {'_id': 0} # suppress id field
                                                            )

        # return None if document does not exist or document has no field with name: field_name
        return document if document else None

    async def get_room_document_id(self, world_name: str, coordinates: list):
        key = await self.database[world_name].find_one({'coordinates': coordinates},
                                                       {'_id': 1} # ony bring back id field
                                                       )

        return key if key else None


    async def room_chatlog_add(self, world_name: str, coordinates: list, chat_name: str, log, max_log_size=20):

        await self.database[world_name].update_one({'coordinates': coordinates}, # update the room at coords
                                                   {'$push': { # specify operation as 'push element into array'
                                                              f'chatlog.{chat_name}' : { # the path to the array (. as seperator in path)
                                                                                        '$each': [log], # each of these elements, needed for slice
                                                                                        '$slice': -max_log_size # ensure the max size is at most this many  of the LATEST elements
                                                                                        }
                                                              }
                                                    },
                                                   upsert=True # if the array does not exist yet, create it before performing the operations
                                                   )