#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 15:45:33 2021

@author: AzureDVBB
"""

import traitlets

class Document:

    __collection: str = None
    __key: str = None
    __data: dict = {}


    def __init__(self, collection: str, key: str, data: dict):
        self.__collection = collection
        self.__key = key
        self.__data = data