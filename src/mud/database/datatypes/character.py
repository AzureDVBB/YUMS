#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 13:01:10 2020

@author: AzureD
"""

from dataclasses import dataclass, asdict

# typing
from .location import Location

@dataclass
class CharacterDocument:
    """
    Document holding all information of a character that's stored in the database.
    """

    name: str
    credentials: dict # TODO: create datatype for credentials
    location: Location

    @property
    def asdict(self) -> dict: # converts to a dictionary to store in database
        return asdict(self)

    @staticmethod
    def from_dict(char_doc: dict):
        return CharacterDocument(char_doc['name'],
                                 char_doc['credentials'],
                                 Location.from_dict(char_doc['location'])
                                 )


@dataclass
class CharacterData:
    """
    Class holding all information of a character loaded into memory and used by the MUD server.
    """

    name: str
    location: Location