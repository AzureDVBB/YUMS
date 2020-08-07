#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 09:56:53 2020

@author: AzureD
"""

from mud.password_hasher import PasswordHasher
from mud import text

# type hints and IDE help
from mud.connection import Connection

class Authentication:

    def __init__(self, database):

        self.database = database
        self.password_hasher = PasswordHasher()


    async def login(self, name: str, password: str): # pass in initialized database class
        if await self.database.character_helper_methods.exists(name):
            credentials = await self.database.character_helper_methods.get_credentials(name)

            valid = await self.password_hasher.validate_credentials_with_password(password, credentials)

            if valid:
                character_data = await self.database.character_helper_methods.get_document(name)
                return (character_data, f"Login succeeded! Welcome to the game {character_data['name']}")

            else:
                return (False, f"Login error: password is invalid")

        else:
            return (False, f"Login error: there is no character with the name '{name}'")


    async def register(self, name: str, password: str):
        if not await self.database.character_helper_methods.exists(name):
            credentials = await self.password_hasher.generate_credentials_with_password(password)

            return await self.database.character_helper_methods.create_new(name, credentials,
                                                                           extra_information=None) # TODO: add extra information (dict)

        else:
            return (False, f"Registraton error: A character by the name {name} allready exists.\r\n"
                    f"Note that capitalization doesn't matter.")


    async def authenticate_connection(self, connection: Connection, max_attempts = 5):
        attempts = 0

        while attempts < max_attempts:
            await connection.write_queue.put(f"{max_attempts - attempts} attempts remaining")
            cmd = await connection.read_queue.get()
            segmented_command = text.split.cleanly(cmd)

            if len(segmented_command) != 3:
                attempts +=1
                await connection.write_queue.put(f"Command error: not understood {cmd}")
                continue

            command, name, password = segmented_command
            if command == 'login':
                result, message = await self.login(name, password)
                await connection.write_queue.put(message)
                if not (result is False):
                    return result # returns the fetched character data from database
                    break
                else:
                    attempts += 1

            elif command == 'register':
                await connection.write_queue.put(f"You are attempting to register with...\r\n"
                                                 f"name: {name}\r\n"
                                                 f"password: {password}\r\n"
                                                 f"Is this correct? Type: 'yes' or 'y' to confirm. "
                                                 f"Or cancel by typing 'no' 'n' or "
                                                 f"anything else really.")

                answer = await connection.read_queue.get()
                if answer.strip().lower() in ('yes', 'y'):
                    result, message = await self.register(name, password)
                else:
                    result = False
                    message = "Aborting..."
                await connection.write_queue.put(message)

                if result:
                    attempts = 0
                    continue
                else:
                    attempts += 1
                    continue

        connection.is_alive = False
        return None