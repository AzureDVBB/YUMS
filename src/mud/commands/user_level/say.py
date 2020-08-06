#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 10:19:13 2020

@author: AzureD
"""

async def handle(player, database, message: str):

    log_entry = {'name': player.name,
                 'time': None, # TODO: add the current server time on it
                 'type': 'say',
                 'message': message
                 }

    await database.world_helper_methods.room_chatlog_add('tutorial', # TODO: use player world name
                                                         player.location,
                                                         'rp', # TODO: figure out the chat channel
                                                         log_entry)

    return None

COMMANDS = {'say': handle}