#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 10:46:16 2020

@author: AzureD

Useful tools to splitting and cleaning up input text.
"""

def cleanly(text: str):
    """
    Splits the text into words at spaces, removing excess spaces.
    """
    segmented = text.split(' ')
    clean = [s for s in segmented if not s == '']
    return clean

def prefix(text: str): # NOTE: PEP 616 solved this in python version 3.9+
    """
    Takes the first word off the text, strips excess spaces and makes sure to always return
    a list containing a prefix, remainder pair of strings.
    """
    segmented = text.split(' ', 1)
    # ensure a list of 2 elements unpacked into a prefix, remainder (even if remainder is nothing)
    prefix, remainder = segmented if len(segmented) == 2 else [text, '']
    return(prefix, remainder.lstrip()) # lstrip removes excess spaces from remainder

def command(text: str):
    """
    Separates and cleans the command(prefix) from a given text, and lower cases it,
    returning both the command and the remaining text
    """
    command, remainder = prefix(text)
    return(command.lower(), remainder)