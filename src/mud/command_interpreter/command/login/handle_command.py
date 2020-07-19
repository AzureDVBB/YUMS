#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:45:07 2020

@author: AzureDVBB
"""

from . import as_guest

OPTIONS = {as_guest.OPTION: as_guest.Guest}
INFO = "To log in type\\r\\nlogin guest <name>"

def handle(subcommand: str):
    temp = subcommand.split(' ', 1)

    if len(temp) == 1:
        return (False, "Login Error: expected login <option> <name> but only '"+
                subcommand+"' was recieved.")

    option, value = temp
    option = option.lower() # ensure lower case characters

    if option in OPTIONS:
        if len(value) < 50:
            return (True, OPTIONS[option](value))
        else:
            return (False,
                    "Login Error: Name too long, please use names that are less then 50 characters.")
    else:
        return (False, "Login Error: Login option '" + temp[0] + "' is not understood. \\r\\n"+
                "Possible options for Login: " + ', '.join(OPTIONS))