#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:45:07 2020

@author: AzureDVBB
"""

from . import as_guest

OPTIONS = {as_guest.OPTION: as_guest.Guest}
INFO = "To log in type\r\nlogin guest <name>"

def handle(option, value):
    if option in OPTIONS:
        if len(value) < 50:
            return OPTIONS[option](value)
        else:
            return (False,
                    "Error: Name too long, please restrict your guest name to 50 characters long.")
    else:
        return (False, "Error: Login option: " + option + " is not understood. \\r\\n"+
                "Possible options for Login: " + ', '.join(OPTIONS))
