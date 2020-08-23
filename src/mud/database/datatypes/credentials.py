#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:05:46 2020

@author: AzureD
"""
from dataclasses import dataclass, asdict


@dataclass
class ScryptArguments:
    """
    Function arguments in the 'Scrypt' hashing alrgorithm determining the hashing difficulty, that is
    the processing time and memory requirements, and the length of the derived hash in bytes.
    """

    # assignments mean default values
    n: int = 32768 # has to be a power of 2
    r: int = 11
    p: int = 1
    maxmem: int = 80000000
    dklen: int = 128 # length of generated key in bytes

    @property
    def asdict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(dictionary: dict):
        return ScryptArguments(dictionary['n'],
                               dictionary['r'],
                               dictionary['p'],
                               dictionary['maxmem'],
                               dictionary['dklen']
                               )


@dataclass
class Credentials:
    """
    Credential data stored inside the database, including the password hash, the salt and scrypt
    arguments.
    """

    password_hash: bytes
    salt: bytes
    scrypt_arguments: ScryptArguments

    @property
    def asdict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(dictionary: dict):
        return Credentials(dictionary['password_hash'],
                           dictionary['salt'],
                           ScryptArguments(dictionary['scrypt_arguments'])
                           )