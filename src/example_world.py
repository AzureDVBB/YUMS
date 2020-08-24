#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:02:16 2020

@author: AzureD

An example world to insert into a fresh MongoDB database so things work nicely out of box.
"""

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
client.drop_database('test-world')
world = client['test-world']['tutorial']

tutorial = [{'coordinates': {'x': 0, 'y': 0, 'z': 0}, # XY coords
             'description': "In the beginning, there was only the soft haze of the misty universe...",
             'connections': {'s': {'x': 1, 'y': 2, 'z': 0}},
             'chatlog': {}
             },
            {'coordinates': {'x': 1, 'y': 1, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'s': {'x': 1, 'y': 2, 'z': 0}, 'e': {'x': 2, 'y': 1, 'z': 0}},
             'chatlog': {}
             },
            {'coordinates': {'x': 1, 'y': 2, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'s': {'x': 1, 'y': 3, 'z': 0}, 'e': {'x': 2, 'y': 2, 'z': 0},
                             'n': {'x': 1, 'y': 1, 'z': 0}
                             },
             'chatlog': {}
             },
            {'coordinates': {'x': 1, 'y': 3, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'n': {'x': 1, 'y': 2, 'z': 0}, 'e': {'x': 2, 'y': 3, 'z': 0}},
             'chatlog': {}
             },
            {'coordinates': {'x': 2, 'y': 1, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': {'x': 1, 'y': 1, 'z': 0}, 'e': {'x': 3, 'y': 1, 'z': 0},
                             's': {'x': 2, 'y': 2, 'z': 0}
                             },
             'chatlog': {}
             },
            {'coordinates': {'x': 2, 'y': 2, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': {'x': 1, 'y': 2, 'z': 0}, 'e': {'x': 3, 'y': 2, 'z': 0},
                             's': {'x': 2, 'y': 3, 'z': 0}, 'n': {'x': 2, 'y': 1, 'z': 0}
                             },
             'chatlog': {}
             },
            {'coordinates': {'x': 2, 'y': 3, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': {'x': 1, 'y': 3, 'z': 0}, 'e': {'x': 3, 'y': 3, 'z': 0},
                             'n': {'x': 3, 'y': 2, 'z': 0}
                             },
             'chatlog': {}
             },
            {'coordinates': {'x': 3, 'y': 1, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': {'x': 2, 'y': 1, 'z': 0}, 's': {'x': 3, 'y': 2, 'z': 0}
                             },
             'chatlog': {}
             },
            {'coordinates': {'x': 3, 'y': 2, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': {'x': 2, 'y': 2, 'z': 0}, 'n': {'x': 3, 'y': 1, 'z': 0},
                             's': {'x': 3, 'y': 3, 'z': 0}
                             },
             'chatlog': {}
             },
            {'coordinates': {'x': 3, 'y': 3, 'z': 0}, # XY coords
             'description': "All you see before you is but a never ending fog of swirling mist.",
             'connections': {'w': {'x': 2, 'y': 3, 'z': 0}, 'n': {'x': 3, 'y': 2, 'z': 0}},
             'chatlog': {}
             }
            ]

print(world.insert_many(tutorial).inserted_ids)
print(client['test-world']['tutorial'].find_one({'coordinates': {'x': 2, 'y': 2, 'z': 0}}))
