#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:44:31 2020

@author: AzureDVBB

description:
All command codes used by the TELNET protocol.

There are also pre-programmed commands with the sent commands and expected responses.
"""

class Code:
    """
    Telnet command codes from https://users.cs.cf.ac.uk/Dave.Marshall/Internet/node141.html
    along side the explanations found as docstrings for easier interpretation.
    """

    SE = 240
    """
    End of subnegotiation parameters.
    """

    NOP = 241
    """
    No operation.
    """

    DM = 242
    """
    Data mark. Indicates the position of a Sync event within the data stream.
    This should always be accompanied by a TCP urgent notification.
    """

    BRK = 243
    """
    Break. Indicates the "break" or "attention" key was hit.
    """

    IP = 244
    """
    Suspend, interrupt or abort the process to which the NVT is connected.
    """

    AO = 245
    """
    Abort output. Allows the current process to run to completion but do not send
    its output to the user.
    """

    AYT = 246
    """
    Are you there? Send back to the NVT some visible evidence that the AYT was recieved.
    """

    EC = 247
    """
    Erase character. The reciever should delete the last preceding character from
    the data stream.
    """

    EL = 248
    """
    Erase line. Delete characters from the data stream back to but not including
    the previous CRLF (carriage return, line feed).
    """

    GA = 249
    """
    Go ahead. Used under certain circumstances, to tell the other end that it can transmit.
    """

    SB = 250
    """
    Subnegotiation of the indicated option follows.
    """

    WILL = 251
    """
    Indicates the desire to begin performing, or confirmation that you are
    performing, the indicated option.
    """

    WONT = 252
    """
    Indicates the refusal to perform, or continue performing, the indicated option.
    """

    DO = 253
    """
    Indicates the request that the other party perforn, or confirmation that you are
    expecting the other party to perform, the indicated option.
    """

    DONT = 254
    """
    Indicates the demand that the other party stop performing, or confirmation that you
    longer expecting the other party to perform, the indicated option.
    """

    IAC = 255
    """
    Interpret as command.
    """

class Command:
    """
    Programmed in TELNET commands with the codes required to send (request) and their
    expected responses (response).
    """

    class are_you_there: # FIXME: sending it a second time in 20s will cause it to be ignored
        """Request and Response codes for the check to see if the client is still connected."""

        request = bytes([Code.IAC, Code.DO, Code.AYT])
        """Command to request to check if the client is still alive."""

        response = bytes([Code.IAC, Code.WONT, Code.AYT])
        """Response to the check to see if the client is alive."""