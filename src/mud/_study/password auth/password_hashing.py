#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 09:41:54 2020

@author: AzureD

Experimenting with securely storing passwords as hashes.

a useful resource is : https://cryptobook.nakov.com/mac-and-key-derivation/scrypt
"""

from hashlib import scrypt # python secure hashing with salt and difficulty options
from os import urandom
import timeit

pwd = "Hello World!"

def pwd():
    # salt: the random number used to randomize the hashes, making cracking it immesurably harder
    # n: CPU/memory cost factor, must be a power of 2
    # r: the block size
    # p: parallelization factor
    # maxmem: the maximum memory used
    # dklen: length of the derived hash
    return scrypt(b"Hello World!", salt=urandom(512), n=(32768), r=11, p=1, maxmem=80000000, dklen=512)

def pwd_hash(pwd, salt):
    return scrypt(pwd.encode(), salt, n=32768, r=11, p=1, maxmem=80000000, dkeylen=512)

# time the hashing function
print(f"{round(timeit.timeit(pwd, number=100)/100, 6)} s")