#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:14:32 2020

@author: AzureD

Functions for registration and login.
"""

async def login(name, password, database, password_hasher): # pass in initialized database class
    if await database.character.exists(name):
        credentials = await database.character.get_credentials(name)

        valid = await password_hasher.validate_credentials_with_password(password, credentials)

        if valid:
            character_data = await database.character.get_document(name)
            return (character_data, f"Login succeeded! Welcome to the game {character_data['name']}")

        else:
            return (False, f"Login error: password is invalid")

    else:
        return (False, f"Login error: there is no character with the name '{name}'")

async def register(name, password, database, password_hasher):
    if not await database.character.exists(name):
        credentials = await password_hasher.generate_credentials_with_password(password)

        await database.character.create_new(name, credentials,
                                            extra_information=None) # TODO: add extra information (dict)
        return (True, f"Registration succeeded! You may now log in {name}")

    else:
        return (False, f"Registraton error: A character by the name {name} allready exists.\r\n"
                f"Note that capitalization doesn't matter.")