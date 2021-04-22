#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:05:28 2020

@author: AzureD
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importer import DummyMain

class Dummy:

    def __init__(self, dummy_ref: DummyMain):
        self.dummy_ref = dummy_ref