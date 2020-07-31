#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:38:36 2020

@author: AzureD

Testing reloading of modules during runtime to commit changes made without restarting scripts.
"""

import time
import importlib

import testing # load test module
import packtest # load test package

variable_example = testing.run # test if taken references will change

def reload_all():
    importlib.reload(testing)
    importlib.reload(packtest)

while True:
    variable_example()
    testing.run()
    packtest.testing.run()
    time.sleep(10)
    reload_all()
