#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:05:14 2020

@author: AzureD
"""

class DummyMain:

    def __init__(self):
        from imported import Dummy
        self.dummy = Dummy(self)