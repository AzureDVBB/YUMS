#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 12:37:55 2020

@author: AzureD

A collection of useful functions for interpreting commands.
"""

def separate_prefix(message: str):
    """
    Takes the first word off the message, strips excess spaces and makes sure to always return
    a list containing a prefix, message pair of strings.
    """
    segmented = message.split(' ', 1)
    # ensure a list of 2 elements unpacked into a command and a value
    command, value = segmented if len(segmented) == 2 else [message, '']
    return(command.strip(), value.lstrip())

def split_cleanly(message: str):
    """
    Splits the message into words, leaving out extra spaces.
    """
    segmented = message.split(" ")
    clean = [s for s in segmented if not s == '']
    return clean