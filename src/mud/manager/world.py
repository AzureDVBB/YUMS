#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:54:47 2020

@author: AzureD
"""

# import for type hinting and IDE help
from mud.player import Player


class World:

    def __init__(self):
        self.__world = {} # container for the rooms that hold players


    def add_player(self, player: Player):
        world_name = player.location.world_name
        coordinates = player.location.coordinates

        # add world name key to dictionary by assigning another empty dictionary to it
        if not world_name in self.__world:
            self.__world[world_name] = {}

        # add player list if not coordinates not allready in world
        if not coordinates in self.__world[world_name]:
            self.__world[world_name][coordinates] = []

        # add player to the list of players currently inside the location
        self.__world[world_name][coordinates].append(player)


    def remove_player(self, player: Player):
        world_name = player.location.world_name
        coordinates = player.location.coordinates

        # remove player from the world location they are in, if they are actually in there
        if world_name in self.__world and coordinates in self.__world[world_name]: # ensure keys exist
            if player in self.__world[world_name][coordinates]: # ensure player is inside the room
                self.__world[world_name][coordinates].remove(player) # remove from list

        # check if location coordinates have no players and remove it if so
        if not self.__world[world_name][coordinates]:
            del self.__world[world_name][coordinates]

        # check if world contains no coordinates that have players, remove it if so
        if not self.__world[world_name]:
            del self.__world[world_name]


    # HANDLED IN 'mud/player.py'
    # def move_player(self, player: Player, new_location: Location):
    #     self.remove_player(player)
    #     player.location = new_location
    #     self.add_player(player)