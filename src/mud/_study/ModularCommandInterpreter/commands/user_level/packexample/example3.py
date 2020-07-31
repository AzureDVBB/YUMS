#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:26:40 2020

@author: AzureD
"""

# import all necessary helper modules needed for this one to function
from . import helper
# Do note: The modules imported here will be immediately reloaded as a side effect

### Add runtime reloading support for importing helper modules ############
###########################################################################
import importlib as __importlib # importlib module aliased

__MODULES = [helper] # list all module references used to enable runtime reload support for them

for __m in __MODULES: # run through each module and
    __importlib.reload(__m) # reload the module

del __m, __MODULES # remove unneeded variables
###########################################################################

print("Loaded user/example3")

def run(player, database, message):
    print("Run user/example3")
    helper.helping()

COMMANDS = {'example3': run}