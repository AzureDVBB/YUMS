#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:04:10 2020

@author: AzureD
"""

from dataclasses import dataclass, asdict

@dataclass
class Coordinates:
    """
    The uh... X Y Z coordinates... Nothing special. Mostly just more convenient then a dictionary.
    """

    __slots__ = ['x', 'y', 'z']

    x: int
    y: int
    z: int


    @property
    def asdict(self) -> dict: # converts to a dictionary to store in database
        return asdict(self)


    ### make hashable to enable using it as dictionary keys #######################################
    def __eq__(self, other): # define equality checking as hash needs it
        return self.x == other.x and self.y == other.y and self.z == other.z


    def __hash__(self): # define hash as the hash of the dict representation's string
        return hash(str(self.asdict))
    ###############################################################################################


    @staticmethod
    def from_dict(coords: dict):
        return Coordinates(coords['x'], coords['y'], coords['z'])


@dataclass
class Location:
    """
    Location data that is stored on the database, including the name of the world the location is in,
    and its X Y Z coordinates.
    """

    __slots__ = ['world_name', 'coordinates'] # limit variable names to save memory

    world_name: str
    coordinates: Coordinates

    @property
    def asdict(self) -> dict: # converts to a dictionary to store in database
        return asdict(self)


    @staticmethod
    def from_dict(location: dict):
        return Location(location['world_name'],
                        Coordinates.from_dict(location['coordinates'])
                        )