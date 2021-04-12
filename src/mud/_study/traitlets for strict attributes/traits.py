#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 11:42:07 2021

@author: AzureDVBB
"""
from dataclasses import dataclass

from traitlets import HasTraits, TraitType, TraitError
from traitlets import Dict, Int, Float, Bool, Unicode, Enum
from traitlets import validate, observe

######################################################################################
# custom trait type
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

##################################################################################
# having traits on a class with custom validation
# unfortunately this has a few caveats, including alot of class methods being inherited
class Traditional(HasTraits):

    name = Ascii(help="Character name, cannot have spaces and has to be ASCII characters only")
    level = Int()

    @validate('name')
    def __validate_name(self, proposal):
        if not ' ' in proposal.value:
            # ensure immutability after setting the trait for the first time
            if not proposal.trait.read_only:
                proposal.trait.read_only = False # set to true if you want name to be locked readonly

            return proposal.value

        raise TraitError('Spaces are not allowed in character names.')

    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

##############################################################################################
# a more compartmentalized way to access traits, each trait has its own class container
# unfortunately this is a rather cumpersome and tedius way of programming so it is not recommended

# name trait container
class CompName(HasTraits):
    name = Ascii(help="Character name, cannot have spaces and has to be ASCII characters only")

    @validate('name')
    def __validate_name(self, proposal):
        if not ' ' in proposal.value:
            # ensure immutability after setting the trait for the first time
            if not proposal.trait.read_only:
                proposal.trait.read_only = False # set to true if you want name to be locked readonly

            return proposal.value

        raise TraitError('Spaces are not allowed in character names.')

# level container
class CompLevel(HasTraits):
    level = Int()

# container dataclass for holding the compartmentalized traits
class Compartmentalized:
    __hidden_attributes = {'name': CompName(), 'level': CompLevel()}
    name: CompName
    level: CompLevel

    def __getattr__(self, attrname):
        if attrname in self.__hidden_attributes:
            return getattr(self.__hidden_attributes[attrname], attrname)
        else:
            raise AttributeError(f"No such attribute with name '{attrname}'")

    def __setattr__(self, attrname, newval):
        if attrname in self.__hidden_attributes:
            setattr(self.__hidden_attributes[attrname], attrname, newval)
        else:
            raise AttributeError(f"No such attribute with name '{attrname}'")

    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

############################################################################################
# a wrapper around the traditional way to make IDE's more happy and show type hints while still
# allowing full traitlets functionality

# write the function as normal with the traits
class Wrappee(HasTraits):

    name = Ascii(help="Character name, cannot have spaces and has to be ASCII characters only")
    level = Int()

    @validate('name')
    def __validate_name(self, proposal):
        if not ' ' in proposal.value:
            # ensure immutability after setting the trait for the first time
            if not proposal.trait.read_only:
                proposal.trait.read_only = False # set to true if you want name to be locked readonly

            return proposal.value

        raise TraitError('Spaces are not allowed in character names.')

    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

# write a wrapper for it, using property getters and setters in order to control how access is done
# this is a dumb and slow way to do things, however it is nearly guaranteed to work, hides all
# the messy methods that traitlets put on the class, and IDE's hinting will always be able to
# help developers with it.
#
# in short, it's dumb but it works beautifully in hiding any messy trait objects

class Wrapped:

    def __init__(self, name: str, level: int):
        self._wrapped = Wrappee(name, level)

    @property
    def name(self):
        return self._wrapped.name
    @name.setter
    def name(self, newval):
        self._wrapped.name = newval

    @property
    def level(self):
        return self._wrapped.level
    @level.setter
    def level(self, newval):
        self._wrapped.level = newval

###################################################################################################
# descriptor pattern described at >>>>>>> https://docs.python.org/3/howto/descriptor.html

# descriptor class for the same ASCII trait
class DescAscii:
    """A string of strictly ASCII characters."""

    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'
        self.public_name = f'{name}'

    def __get__(self, instance, owner=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value.encode('ascii')
                setattr(instance, self.private_name, value)
            except UnicodeEncodeError:
                raise AttributeError(f"Descriptor '{self.public_name}' cannot contain non-ASCII characters not: {type(value)}( {value} )")
        else:
            raise AttributeError(f"Descriptor '{self.public_name}' has to be of type 'str' not: {type(value)}( {value} )")

# descriptor class for the same INT trait
class DescInt:
    """A strictly integer attribute."""

    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'
        self.public_name = f'{name}'

    def __get__(self, instance, owner=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        if isinstance(value, int):
            setattr(instance, self.private_name, value)
        else:
            raise AttributeError(f"Descriptor '{self.public_name}' has to be of type 'int' not: {type(value)}( {value} )")


# putting it together
class Descriptorized:
    name = DescAscii()
    level = DescInt()

    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

# testing stuff
# tw = Traditional('derg', 1)
# cp = Compartmentalized('derg', 1)
# wp = Wrapped('derg', 1)
# dd = Descriptorized("vetu", 1)