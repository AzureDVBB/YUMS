#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 23:31:02 2020

@author: AzureD

Helper functions for painless database accessing for common things. Now fully asynchronous!
"""

import motor.motor_asyncio as motor

client = motor.AsyncIOMotorClient('mongodb://localhost:27017') # change this for the database host

__user_database_name = "test-users" # the database name where all user data is stored
__character_collection_name = "test-characters" # collection where individual characters and login is stored
__account_collection_name = "test-accounts" # collection where individual player accounts are stored

__character_collection = client[__user_database_name][__character_collection_name]
__account_collection = client[__user_database_name][__user_database_name]

async def get_character_credentials(name: str):
    user = await __character_collection.find_one(name)
    return None if user is None else {'name': user['name'],
                                      'salt': user['salt'],
                                      'password hash': user['password hash']}

async def check_character_name_existance(name: str):
    character = await __character_collection.find_one(name)
    return False if character is None else True

async def create_new_character(name: str, salt: bytes, password_hash: bytes,
                               extra_information: dict=None):
    exists = check_character_name_existance(name)
    if not exists:
        new_character = {'name': name, 'salt': salt, 'password hash': password_hash}
        if extra_information: # it is not None
            new_character.update(extra_information)
        await __character_collection.insert(new_character)
        return True
    else:
        return False