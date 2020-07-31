#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 23:31:02 2020

@author: AzureD

Helper functions for painless database accessing for common things. Now fully asynchronous!
"""
import asyncio
import motor.motor_asyncio
# client = pymongo.MongoClient('mongodb://localhost:27017')


class Database:

    __user_database_name = "test-users" # the database name where all user data is stored
    __character_collection_name = "test-characters" # collection where individual characters and login is stored
    __account_collection_name = "test-accounts" # collection where individual player accounts are stored

    __world_database_name = "test-world" # the database name where all world data is kept
    __tutorial_collection_name = "tutorial" # the name of the collection where the tutorial is stored

    def __init__(self):
        """
        Initialize the asynchronous client for the database inside the running eventloop.
        Due to the import happening before the event loop being established
        this init function must be called from the main server function to ensure
        the correct and running event loop is being passed on.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017',
                                                        io_loop=asyncio.get_running_loop())

        self.__character_collection = self.client[Database.__user_database_name][Database.__character_collection_name]
        self.__account_collection = self.client[Database.__user_database_name][Database.__user_database_name]

        self.__tutorial_collection = self.client[Database.__world_database_name][Database.__tutorial_collection_name]


    async def __get_character_data(self, name: str):
        return await self.__character_collection.find_one({'name': name})

    async def get_character_credentials(self, name: str):
        user = await self.__get_character_data(name)
        return None if user is None else {'salt': user['salt'],
                                          'password hash': user['password hash']}

    async def is_existing_character(self, name: str):
        character = await self.__get_character_data(name)
        return False if character is None else True

    async def create_new_character(self, name: str, salt: bytes, password_hash: bytes,
                                   extra_information: dict=None):
        if not await self.is_existing_character(name):
            new_character = {'name': name, 'salt': salt, 'password hash': password_hash,
                             'location': [2,2]} # TODO: set new player location
            if extra_information: # it is not None
                new_character.update(extra_information)
            await self.__character_collection.insert_one(new_character)
            return True
        else:
            return False

    async def get_character_game_data(self, name: str):
        if await self.is_existing_character(name):
            character = await self.__get_character_data(name)
            return {'name': character['name'], 'location': character['location']}
        else:
            return None

    async def get_room_by_id(self, room_id):
        return await self.__tutorial_collection.find_one({'room_id': room_id})
