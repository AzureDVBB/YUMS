#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:55:37 2020

@author: AzureDVBB
"""

async def echo(database, manager, player, message):
    player.send(message)

    return None # to use AWAIT with this and pause command watchdog for players, needs a return


# make sure to have the COMMANDS dictionary at the end of the file to house all defined commands
COMMANDS = {'echo': echo}