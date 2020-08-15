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

    name: str
    credentials: dict # TODO: create datatype for credentials
    location: Location

    @property
    def asdict(self): # converts to a dictionary to store in database
        return asdict(self)

    def from_dict(self, char_doc: dict):
        return CharacterDocument(char_doc['name'],
                                 char_doc['credentials'],
                                 Location.from_dict(char_doc['location'])
                                 )


@dataclass
class CharacterData:

    name: str
    location: Location