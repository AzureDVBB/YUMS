#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 21:18:10 2020

@author: AzureD
"""
from mud.database import Database
from mud.player import Player

class ChatManager:

    def __init__(self, database: Database):

        self.database = database
        self.global_chats = {}


    def add_player_to_channel(self, player: Player, channel_name: str):

        if not channel_name in self.global_chats: # create list at key if key did not exist yet
            self.global_chats[channel_name] = []

        self.global_chats[channel_name].append(player)


    def remove_player_from_channel(self, player: Player, channel_name: str):

        self.global_chats[channel_name].remove(player)

        if not self.global_chats[channel_name]: # delete unused channels
            del self.global_chats[channel_name]


    def send_message_to_channel(self, channel_name: str, message: str):

        for player in self.global_chats[channel_name]:
            player.send(message)

        return None # needed for async def