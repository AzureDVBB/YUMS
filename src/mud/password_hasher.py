#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:56:07 2020

@author: AzureD

Async ready password hasher, due to it being blocking it runs in a seperate process pool.
"""
import asyncio
from concurrent.futures import ProcessPoolExecutor
from hashlib import scrypt
from os import urandom

def blocking_hash_password_with_salt(args):
        password, salt = args
        # tune parameters for desired difficulty
        return scrypt(password.encode(), salt=salt, n=32768, r=11, p=1, maxmem=80000000, dklen=128)

class PasswordHasher:

    def __init__(self):
        self.__loop = asyncio.get_running_loop() # the currently running eventloop
        self.__executor = ProcessPoolExecutor(max_workers=1) # worker process pool

    @staticmethod
    def generate_salt(length_bytes = 128):
        return urandom(length_bytes)

    async def hash_password_with_salt(self, password: str, salt: bytes):
        return await self.__loop.run_in_executor(self.__executor,
                                                 blocking_hash_password_with_salt,
                                                 (password, salt))

    async def validate_password_salt_hash(self, password: str, salt: bytes,
                                          hashed_salted_password: bytes):

        password_hashed = await self.hash_password_with_salt(password, salt)
        return hashed_salted_password == password_hashed