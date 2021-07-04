#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 21:40:02 2021

@author: AzureDVBB
"""

from document import Document


class KeyValueDatabase:

    _dbname: str # name of the key value database (called a 'collection' in the document storage)
    _kvnamespace: str # namespace of the key-value storage (identifying the document storing k:v pairs)

    _containerdoc: Document # container document where all the data actually lives

    def __init__(self, dbname: str, kvnamespace: str):
        self._dbname = dbname
        self._kvnamespace = kvnamespace
        self._containerdoc = Document(dbname, kvnamespace, True)

    def __getitem__(self, key: str):
        return self._containerdoc[key]

    def __setitem__(self, key: str, value):
        self._containerdoc[key] = value

    def __delitem__(self, key: str):
        del(self._containerdoc[key])

    def __contains__(self, key: str):
        return key in self._containerdoc
