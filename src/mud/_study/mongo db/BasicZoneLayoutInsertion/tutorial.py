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

tutorial = [{'coordinates': [0,0,0], # XY coords
             'description': "In the beginning, there was only the soft haze of the misty universe...",
             'connections': {'s': [1,2,0]},
             'chatlog': {}
             },
            {'coordinates': [1,1,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'s': [1,2,0], 'e': [2,1,0]},
             'chatlog': {}
             },
            {'coordinates': [1,2,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'s': [1,3,0], 'e': [2,2,0], 'n': [1,1,0]},
             'chatlog': {}
             },
            {'coordinates': [1,3,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'n': [1,2,0], 'e': [2,3,0]},
             'chatlog': {}
             },
            {'coordinates': [2,1,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [1,1,0], 'e': [3,1,0], 's': [2,2,0]},
             'chatlog': {}
             },
            {'coordinates': [2,2,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [1,2,0], 'e': [3,2,0], 's': [2,3,0], 'n': [2,1,0]},
             'chatlog': {}
             },
            {'coordinates': [2,3,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [1,3,0], 'e': [3,3,0], 'n': [3,2,0]},
             'chatlog': {}
             },
            {'coordinates': [3,1,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [2,1,0], 's': [3,2,0]},
             'chatlog': {}
             },
            {'coordinates': [3,2,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [2,2,0], 'n': [3,1,0], 's': [3,3,0]},
             'chatlog': {}
             },
            {'coordinates': [3,3,0], # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': [2,3,0], 'n': [3,2,0]},
             'chatlog': {}
             }
            ]

print(world.insert_many(tutorial).inserted_ids)
print(client['test-world']['tutorial'].find_one({'coordinates': [2,2,0]}))