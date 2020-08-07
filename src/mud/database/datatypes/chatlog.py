#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:05:37 2020

@author: reevi
"""

from dataclasses import dataclass, asdict

@dataclass
class LogEntry:

    character_name: str
    # time: object # TODO: add server time grabbing code
    channel_name: str
    message: str

    @property
    def as_dict(self): # converts to a dictionary to store in database
        return asdict(self)