#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 14:36:34 2020

@author: AzureD

A collection of common database operations abstracted away.

These are related to accessing and manipulating the player character data on the dabase.
"""

from .datatypes import Location, Coordinates, CharacterData, CharacterDocument, Credentials

class Character:

    def __init__(self, collection):
        self.collection = collection


    async def get_document_fields(self, name: str, field_names: list) -> dict:
        whitelisted_fields = {field: 1 for field in field_names} # works like a list comprehension

        document = await self.collection.find_one({'name': name}, # world_name collection in the database
                                                  {'_id': 0, # do not get the document id
                                                   }.update(whitelisted_fields) # add whitelist to dict
                                                  )

        # return None if document does not exist or document has no field with name: field_name
        return document if document else None


    async def get_document(self, name: str) -> dict:
        return await self.collection.find_one({"name": name},
                                              {"_id": 0, "credentials": 0}
                                              )


    async def get_player_data(self, name: str) -> CharacterData:
        ret = await self.get_document_fields(name, ['location'])

        location = Location.from_dict(ret['location'])
        return CharacterData(name, location)


    async def get_credentials(self, name: str) -> Credentials:
        document = await self.get_document_fields(name, 'credentials')
        return Credentials.from_dict(document['credentials'])


    async def exists(self, name: str) -> bool:
        # return True if a non-empty dictionary is returned, False otherwise, for a given name
        return True if await self.get_document_fields(name, "name") else False


    async def create_new(self, name: str, credentials: Credentials, extra_information=None):
        # TODO: add support for extra information during registration
        if await self.exists(name):
            return (False, "ERROR: Character name allready in use.")
        else:
            await self.collection.insert_one({"name": name,
                                              "location": Location("tutorial",
                                                                   Coordinates(0,0,0)
                                                                   ).asdict,
                                              "credentials": credentials.asdict
                                              }
                                             )
            return (True, f"SUCESS: Character created under the name: {name}\r\nYou may now log in.")