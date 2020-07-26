#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 17:16:59 2020

@author: AzureDVBB

The interpreter for all commands.

Each handler must return a touple of two elements:  (return value or object, message to the player)

The return value can be a Boolean True of False, indicating the success/failure of the command
being interpreted, for things that have no return objects/values.
They can also be any value or object that is returned by the command handling modules.

Example: Login returns FALSE on unsuccessful logins, but returns the NAME string if successfully
logging in as a guest, alongside the message explaining to the user what happened.
"""

from .commands import IMPLEMENTED
from .commands.helper_functions import separate_prefix

def interpret(msg: str, player):
    command, value = separate_prefix(msg)

    # prevent program errors due to people logged in trying to login again
    if command in ('login', 'register'):
        return (False, 'Command error: Allready logged in!')

    # player object passed in, commands interpreted for logged-in player
    elif command in IMPLEMENTED:
        return IMPLEMENTED[command](value, player)

    # invalid command handling
    else:
        return(False, f"Command not recognized: {msg}")