#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:40:04 2020

@author: AzureDVBB
"""

OPTION = "guest"

class Guest:

    def __init__(self, name):
        self.name = '[Guest] - '+ name
        self.type = 'guest'
        self.location = None

    @property
    def welcome(self):
        return ("Welcome "+ self.name +" to the game! Hope you have a great day.")