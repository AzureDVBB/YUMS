#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:56:07 2020

@author: AzureD

Async ready password hasher, due to it being blocking it runs in a seperate process pool.
"""
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from hashlib import scrypt
from secrets import token_bytes

# type hinting and IDE stuff
from mud.database.datatypes import Credentials, ScryptArguments

def blocking_hash_password_with_salt(args: dict):
        # unpack the arguments
        password = args['password']
        salt = args['salt']
        if 'srypt arguments' in args.keys(): # test if scrypt arguments supplied
            n = args['scrypt arguments']['n']
            r = args['scrypt arguments']['r']
            p = args['scrypt arguments']['p']
            maxmem = args['scrypt arguments']['maxmem']
            dklen = args['scrypt arguments']['dklen']
        else: # have a default if incorrect dictionary was passed in
            n=32768
            r=11
            p=1
            maxmem=80000000
            dklen=128
        # tune parameters for desired difficulty
        # example tuning: n=32768, r=11, p=1, maxmem=80000000, dklen=128
        return scrypt(password.encode(), salt=salt, n=n, r=r, p=p, maxmem=maxmem, dklen=dklen)

class PasswordHasher:

    def __init__(self):
        self.__loop = asyncio.get_running_loop() # the currently running eventloop

        # WARNING: Process Pool is wonky on windows but fine on linux, using threadpool as workaround

        #self.__executor = ProcessPoolExecutor(max_workers=1) # worker process pool
        self.__executor = ThreadPoolExecutor(max_workers=1) # worker process pool

    @staticmethod
    def generate_salt(length_bytes = 128) -> bytes:
        return token_bytes(length_bytes)


    async def __hash_password_with_arguments(self, arguments: dict):
        return await self.__loop.run_in_executor(self.__executor,
                                                 blocking_hash_password_with_salt,
                                                 arguments
                                                 )

    async def generate_credentials_with_password(self, password: str) -> Credentials:
        salt = self.generate_salt()
        hashing_args = ScryptArguments().asdict
        hashing_args.update({'password': password, 'salt': salt})
        pwd_hash = await self.__hash_password_with_arguments(hashing_args)

        return Credentials(pwd_hash, salt, ScryptArguments())


    async def validate_credentials_with_password(self, password: str, credentials: Credentials) -> bool:
        scrypt_arg_dict = {'password': password,
                           'salt': credentials.salt,
                           'scrypt arguments': credentials.scrypt_arguments.asdict
                           }
        pwd_hash = await self.__hash_password_with_arguments(scrypt_arg_dict)

        if (pwd_hash == credentials.password_hash):
            return True
        else:
            return False