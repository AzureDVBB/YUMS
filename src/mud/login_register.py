#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:14:32 2020

@author: AzureD

Functions for registration and login.
"""

async def login(name, password, database, password_hasher): # pass in initialized database class
    if await database.is_existing_character(name):
        credentials = await database.get_character_credentials(name)
        salt = credentials['salt']
        pwd_hash = credentials['password hash']
        valid = await password_hasher.validate_password_salt_hash(password, salt, pwd_hash)

        if valid:
            character_data = await database.get_character_game_data(name)
            return (character_data, f"Login succeeded! Welcome to the game {character_data['name']}")

        else:
            return (False, f"Login error: password is invalid")

    else:
        return (False, f"Login error: there is no character with the name '{name}'")

async def register(name, password, database, password_hasher):
    if not await database.is_existing_character(name):
        salt = password_hasher.generate_salt()
        pwd_hash = await password_hasher.hash_password_with_salt(password, salt)

        await database.create_new_character(name, salt, pwd_hash,
                                            extra_information=None) # TODO: add extra information (dict)
        return (True, f"Registration succeeded! You may now log in {name}")

    else:
        return (False, f"Registraton error: A character by the name {name} allready exists.\r\n"
                f"Note that capitalization doesn't matter.")