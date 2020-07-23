#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:14:43 2020

@author: AzureD
"""
import pymongo

tutorial_map = pymongo.MongoClient('mongodb://localhost:27017')['test-world']['tutorial']

def no_input(player):
    room = tutorial_map.find_one({'room_id': player.location})
    if room is None:
        return (False, f"Database ERROR: Room not found {player.location}")

    room_id = room['room_id']
    desc = room['description']
    exits = list(room['connections'].keys())

    return (True, f"Room ID: {room_id}\r\n"
            f"{desc}\r\n"
            f"Exits: {exits}")

OPTIONS = {'': no_input}

def handle(message: str, player):
    command = message.lower().strip()
    if command in OPTIONS:
        return OPTIONS[command](player)
    else:
        return (False, f"No such option for: look <option>\r\n"
                f"Possible options: {OPTIONS}\r\n"
                f"Recieved command: {command}")

IMPLEMENTED = {'look': handle}