#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:57:35 2020

@author: AzureD
"""

class World:

    def __init__(self, database):

        self.database = database

    async def __get_room_document_field_in_world_by_coordinates(self, world_name: str,
                                                                coordinates: list, field_name: str):

        return await self.database[world_name].find_one( # world_name collection in the database
                                                        {'coordinates': coordinates}, # get room by id
                                                        {'_id': 0, # do not get the document id
                                                         field_name: 1} # do get the specifiec field
                                                        )


    async def __get_room_document_in_world_by_coordinates(self, world_name: str, coordinates: list):

        return await self.database[world_name].find_one({'coordinates': coordinates},
                                                        {'_id': 0} # suppress id field
                                                        )


    async def get_room_in_world_by_coordinates(self, world_name: str, coordinates):

        return await self.__get_room_document_in_world_by_coordinates(world_name, coordinates)


    async def get_room_connections_in_world_by_coordinates(self, world_name: str, coordinates):

        return await self.__get_room_document_field_in_world_by_coordinates(world_name, coordinates,
                                                                            'connections')