#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 21:18:10 2020

@author: AzureD
"""
from mud.database import Database
from mud.player import Player

#type hinting and IDE
from . import Manager

class ChatManager:

    def __init__(self, main_manager: Manager, database_uri: str):

        self.__database = Database(database_uri)
        self.__main_manager = main_manager
        self.global_chats = {}