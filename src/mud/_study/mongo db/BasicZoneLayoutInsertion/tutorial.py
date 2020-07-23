#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:02:16 2020

@author: AzureD
"""

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
client.drop_database('test-world')
world = client['test-world']['tutorial']

tutorial = [{'room_id': [1,1], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'s': [1,2], 'e': [2,1]}
             },
            {'room_id': [1,2], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'s': [1,3], 'e': [2,2], 'n': [1,1]}
             },
            {'room_id': [1,3], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'n': [1,2], 'e': [2,3]}
             },
            {'room_id': [2,1], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [1,1], 'e': [3,1], 's': [2,2]}
             },
            {'room_id': [2,2], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [1,2], 'e': [3,2], 's': [2,3], 'n': [2,1]}
             },
            {'room_id': [2,3], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [1,3], 'e': [3,1], 'n': [3,3]}
             },
            {'room_id': [3,1], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [2,1], 's': [3,2]}
             },
            {'room_id': [3,2], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [2,2], 'n': [3,1], 's': [3,3]}
             },
            {'room_id': [3,3], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [2,3], 'n': [3,2]}
             }
            ]

print(world.insert_many(tutorial).inserted_ids)
print(client['test-world']['tutorial'].find_one({'room_id': [2,2]}))