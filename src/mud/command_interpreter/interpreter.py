#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 17:16:59 2020

@author: AzureDVBB
"""

from . import command

def analyze(msg):
    text = str(msg).lstrip().strip() # remove all leading (lstrip) and traling (strip) special chars
    segmented = str(msg[:60]).split() # maximum 60 characters for command + option
    if len(segmented) < 3:
        return None
    else:
        return {'command': segmented[0], 'option': segmented[1],
                'value': text[(len(segmented[0])+len(segmented[1])+2):]} # text excluding cmd+option

def interpret(msg):
    r = analyze(msg)
    if r is None:
        return(False, "Unrecognized input.")
    elif r['command'] in command.IMPLEMENTED:
        return command.IMPLEMENTED[r['command']](r['option'], r['value'])
    else:
        return (False, "Unknown command: " + r['command'])