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

def interpret(msg: str, player = None):
    segmented = msg.split(' ', 1)
    # ensure a list of 2 elements unpacked into a command and a value
    command, value = segmented if len(segmented) == 2 else [msg, '']
    command = command.strip().lower()

    # no player object passed to the function, allows only the login command to be used
    if player is None:
        if command == 'login':
            return IMPLEMENTED['login'](value)
        else:
            return (False, "Unrecognized command: " + command + "\r\n" +
                    "Please use either: " + "\r\n" +
                    "login <character name> <password>" + "\r\n"
                    "login guest <guest name>")

    # prevent program errors due to people logged in trying to login again
    elif command == 'login':
        return (False, 'Command error: Allready logged in!')

    # player object passed in, commands interpreted for logged-in player
    elif command in IMPLEMENTED:
        return IMPLEMENTED[command](value)