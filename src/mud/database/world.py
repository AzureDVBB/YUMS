#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:57:35 2020

@author: AzureD
"""

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