#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 14:36:34 2020

@author: AzureD

Database operations on the user database / character collection.
"""

class Character:

    def __init__(self, collection):
        self.collection = collection

    async def get_document_field(self, name: str, field_name: str):
        # TODO: make it accept a list of fields to get and return

        document = await self.collection.find_one({"name": name}, # search for document with field
                                                  {field_name: 1, # return specific field from document
                                                   "_id": 0} # suppress result containing "_id" field
                                                  ) # return only the credentials dict

        # return None if document does not exist or document has no field with name: field_name
        return document[field_name] if document and (field_name in document) else None

    async def get_document(self, name: str):
        return await self.collection.find_one({"name": name},
                                              {"_id": 0, "credentials": 0})

    async def get_credentials(self, name: str):
        return await self.get_document_field(name, "credentials")

    async def get_location(self, name: str):
        return await self.get_document_field(name, "location")

    async def exists(self, name: str):
        # return True if a non-empty dictionary is returned, False otherwise, for a given name
        return True if await self.get_document_field(name, "name") else False

    async def create_new(self, name: str, credentials: dict, extra_information=None):
        # TODO: add support for extra information during registration
        if await self.exists(name):
            return (False, "ERROR: Character name allready in use.")
        else:
            await self.collection.insert_one({"name": name,
                                              "credentials": credentials,
                                              "location": [0, 0, 0] # TODO: update location/use spawn room
                                              }
                                             )
            return (True, f"SUCESS: Character created under the name: {name}\r\nYou may now log in.")
