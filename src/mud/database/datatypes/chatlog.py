#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:05:37 2020

@author: AzureD
"""

from dataclasses import dataclass, asdict

@dataclass
class LogEntry:
    """
    Holds all data saved to the database with a single chat log entry.
    """

    character_name: str
    # time: object # TODO: add server time grabbing code
    message: str

    @property
    def asdict(self) -> dict: # converts to a dictionary to store in database
        return asdict(self)