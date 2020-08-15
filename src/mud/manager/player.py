#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 14:41:02 2020

@author: AzureD
"""
import asyncio

from mud.database import Database

# type hinting and IDE tab completion
from . import Manager
from mud.database.datatypes import CharacterData, Location

class PlayerManager:

    def __init__(self, main_manager: Manager, database_uri: str):
        self.__main_manager = main_manager
        self.__database = Database(database_uri)

        self.__players_by_location = {} # player names by world/coordinates
        self.player_data = {} # player data by player name


    def __remove_location_(self, location: Location):
        world_name, coordinates = location.world_name, location.coordinates
        # remove location if it exists and is empty now
        if not self.__players_by_location[world_name][coordinates]:
            del self.__players_by_location[world_name][coordinates]
            if not self.__players_by_location[world_name]:
                del self.__players_by_location[world_name]


    def __create_location_(self, location: Location):
        world_name, coordinates = location.world_name, location.coordinates
        if not (world_name in self.__players_by_location):
            self.__players_by_location[world_name] = {}
        if not (coordinates in self.__players_by_location[world_name]):
            self.__players_by_location[world_name][coordinates] = []


    async def add_player(self, player_name: str):
        if player_name in self.player_data:
            print(f"PlayerManager.add_player ERROR: '{player_name}' allready "
                  f"added to the player_data dictionary, ignoring"
                  )

        else:
            player_data = await self.__database.character_helper_methods.get_player_data(player_name)
            self.player_data[player_name] = player_data

            world_name, coordinates = player_data.location.world_name, player_data.location.coordinates
            self.__create_location_(player_data.location)
            self.__players_by_location[world_name][coordinates].append(player_name)


    def remove_player(self, player_name: str):
        if player_name in self.player_data:
            # delete player from both dictionaries, keep location for later
            location = self.player_data[player_name].location
            world_name, coordinates = location.world_name, location.coordinates

            del self.player_data[player_name]

            self.__players_by_location[world_name][coordinates].remove(player_name)
            self.__remove_location_(location)

        else:
            print(f"PlayerManager.remove_player ERROR: '{player_name}' is not present in player_data"
                  f" dictionary, ignoring"
                  )


    def get_player_data(self, player_name: str):
        return self.player_data[player_name]


    def get_player_location(self, player_name: str):
        return self.player_data[player_name].location


    def players_in_location(self, location: Location):
        if location.world_name in self.__players_by_location:
            if location.coordinates in self.__players_by_location[location.world_name]:

                return self.__players_by_location[location.world_name][location.coordinates].copy()

        return []


    def is_online(self, player_name: str):
        return player_name in self.player_data


    def move_player(self, player_name, location: Location):
        if not (player_name in self.player_data):
            print(f"PlayerManager.move_player ERROR: '{player_name}' is not present in player_data"
                  f" dictionary, ignoring"
                  )
        else:
            # remove player from present location list
            old_location = self.player_data[player_name].location
            self.__players_by_location[old_location.world_name][old_location.coordinates].remove(player_name)
            self.__remove_location_(old_location)

            # update player location and add them to the new location list
            self.player_data[player_name].location = location
            self.__create_location_(location)
            self.__players_by_location[location.world_name][location.coordinates].append(player_name)
