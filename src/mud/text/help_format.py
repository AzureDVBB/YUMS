#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:54:02 2020

@author: AzureD

Formatting tools for displaying HELP inside the MUD clients.
"""

def docstring_to_help(name: str, docstring: str):
    """
    Converts a function docstring to a more viewable format for MUD clients.
    Mainly used inside `src/mud/commands` commands for quick help documentation in-code.
    """

    split_doc = docstring.split('\n') # split by newline

    # generate the header of the help, and the footer, examples:
    # ------ [ name #help ] ---------------------------
    # -------------------------------------------------
    header = f"""------ [ {name} #help ] -""".ljust(70, "-")
    footer = "".ljust(70, "-")

    split_doc.insert(0, header)
    split_doc.append(footer)

    return "\r\n".join(split_doc) # ensure compatibility with carriage return aswell as newline