#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:44:45 2021

@author: AzureDVBB
"""

from abc import abstractproperty, abstractmethod
import time
import os
import json

from traitlets import HasTraits, TraitType, TraitError
from traitlets import Dict, Int, Float, Bool, Unicode, Enum
from traitlets import validate, observe

# Disk persistance base class (with traits)
class PersistentDocument(HasTraits):
    """
    Persistent object with traitlets.

    Stores trait values on disk and updates it when traits change.

    Reads trait values from disk every 10s, esentially chaching the value of the persistant data
    for a set period of time. This will reduce load on the underlying data store.
    """

    __next_read_presistent_volume = time.time() - 1

    @abstractproperty
    def _filename(self):
        pass

    @abstractmethod
    def __init__(self):
        pass

    def __load_from_persistent_store(self):
        # load dictionary from json file
        recalled = None
        filepath = os.path.join(os.getcwd(), 'stored_data', f'{self.__filename}.json')
        with open(filepath, 'r') as f:
            read = f.read()
            recalled = json.loads(read)

        # refresh non-read only traits, taking the background storage as the ground truth
        traits = self.traits()
        for key in traits:
            if not traits[key].read_only:
                self.set_trait(key, recalled[key])

        # set the time that read cache neeeds reloading on read
        self.__next_read_presistent_volume = time.time() + 10

    def __save_to_persistent_store(self):
        # ensure folder existance
        if not 'stored_data' in os.listdir():
            os.mkdir('stored_data')

        # write data to storage file
        filepath = os.path.join(os.getcwd(), 'stored_data', f'{self._filename}.json')
        with open(filepath, 'w') as f:
            f.write(json.dumps(self.trait_values()))

    def __getitem__(self, key):
        if self.has_trait(key):
            # recalling persistant values here, using the example of a file here but can be database query

            # object requires refresh (caching) from a persistent volume
            if time.time() > self.__next_read_presistent_volume:
                self.__reload_from_persistent_store()

            # return the selected trait
            return self.trait_values()[key]

        raise Exception(f"No trait with name '{key}' found on object '{self}'")

    def __setitem__(self, key, value):
        if self.has_trait(key):

            if not self.traits()[key].read_only:
                self.set_trait(key, value)

                self.__save_to_persistent_store()

                return None

            raise Exception(f"Cannot set trait '{key}' : it is set to read-only.")

        raise Exception(f"No trait '{key}' found on object '{self}'")


# custom trait type that can be shared between many Documents
class Ascii(TraitType):
    """A trait for ASCII strings."""

    info_text = "ASCII only string"

    def validate(self, obj, value):
        if isinstance(value, str):
            try:
                value.encode('ascii')
                return value
            except UnicodeEncodeError:
                self.error(obj, value)
        self.error(obj, value)


# document class inheriting PersistentDocument for disk persistance and implements example attributes
class PlayerDocument(PersistentDocument):
    """An example document with some attributes and disk persistance.

        Attributes:
            name: str
                Ascii string without spaces.

            species: str
                Ascii string that can be any one between ['feline', 'canine', 'avian', 'dragon'].

            level: int
                Integer between values 1 and 10.

    """

    name = Ascii(help="Character name, cannot have spaces and has to be ASCII characters only")

    species = Enum(['feline', 'canine', 'avian', 'dragon'],
                   help="Character species, has to be all lower case."
                   )

    level = Int(default_value=1, help="Character level, minimum value of 1.")

    @property
    def _filename(self):
        return self.name

    def __init__(self, name: str, species: str, level: int):
        # initialize values
        self.name = name
        self.species = species
        self['level'] = level # triggers disk write while setting value like this (because it calls __setitem__)

    @validate('name')
    def __validate_name(self, proposal):
        if not ' ' in proposal.value:
            # ensure immutability after setting the trait for the first time
            if not proposal.trait.read_only:
                proposal.trait.read_only = True

            return proposal.value

        raise TraitError('Spaces are not allowed in character names.')

    @validate('level')
    def __validate_level(self, proposal):
        if 1 <= proposal.value <= 10:
            return proposal.value

        raise TraitError('Character level out of bounds, must be between 1 and 10.')