#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 17:16:59 2020

@author: AzureDVBB
"""

from . import command

def interpret(msg: str):
    temp = msg.split(' ', 1)

    if len(temp) == 1: # check if option recieved an single word input
        if msg.lower().strip() in command.IMPLEMENTED:
            return command.IMPLEMENTED[msg.lower().strip()]('')
        return (False, "Unrecognized command: " + msg)

    cmd, value = temp

    cmd = cmd.lower() # ensure command is lower case

    if cmd in command.IMPLEMENTED:
        return command.IMPLEMENTED[cmd](value)
    else:
        return (False, "Unrecognized command: " + cmd)