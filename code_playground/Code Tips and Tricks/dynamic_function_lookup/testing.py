#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:43:26 2020

@author: AzureDVBB

Testing and verifying the dynamic function lookups, testing if they are defined and calling them.
"""

import lookup

print('test1' in lookup.IMPLEMENTED)
print(lookup.IMPLEMENTED['test2']())
print(lookup.IMPLEMENTED['test'].run())