#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 15:45:33 2021

@author: AzureDVBB
"""

class Document:

    _collection: str
    _data: dict # modelled background database store
    _key: str # used to uniquely identify documents

    _modifiablekeys: bool # flag that makes the internal dictionary able to add and delete keys

    def __init__(self, collection: str, key: str, modofiablekeys: bool = False):
        self._collection = collection
        self._modifiablekeys = modofiablekeys
        self._key = key
        self._data = {} # load data here


    # handle the updating and retrieval of document key:val pairs from a background storage
    # as well as adding and removing keys from the document and key membership testing
    def __getitem__(self, key: str):
        # perhaps refresh cached data here
        return self._data[key]

    def __setitem__(self, key: str, value):
        if key in self._data.keys():
            self._data[key] = value
        elif self._modifiablekeys:
            self._data[key] = value
        else:
            raise KeyError(f"'{key}' not found in Document.")

    def __delitem__(self, key: str):
        if self._modifiablekeys:
            del(self._data[key])
        else:
            raise NotImplementedError("modifiablekeys flag is set to false, cannot delete keys.")

    def __contains__(self, key):
        return key in self._data.keys()


class Collection:

    _name: str
    _document_keys: list[str]
    _documents: list[Document]

    def __init__(self, collection_name: str):
        self._name = collection_name
        self._document_keys = []
        self._documents = []

    @property
    def name(self):
        return self._name

    def __setitem__(self, key: str, doc: Document):
        pass