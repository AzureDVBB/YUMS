#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:44:31 2020

@author: AzureDVBB

description:
All command codes used by the TELNET protocol.

There are also pre-programmed commands with the sent commands and expected responses.

It is all done with class methods as properties, so we get support of docstrings as
an excellent way to look up what they do from other modules with your IDE of choice.
"""

class TelnetCommands:
    """
    Programmed in TELNET commands with the codes required to send (request) and their
    expected responses (response)
    """

    class are_you_there:
        """Request and Response codes for the check to see"""
        @property
        def request():
            """Command to request to check if the client is still alive."""
            return CommandCodes.IAC + CommandCodes.DO + CommandCodes.AYT

        @property
        def response():
            """Response to the check to see if the client is alive."""
            return CommandCodes.IAC + CommandCodes.WONT + CommandCodes.AYT


class CommandCodes:
    """
    Telnet command codes from https://users.cs.cf.ac.uk/Dave.Marshall/Internet/node141.html
    along side the explanations found as docstrings for easier interpretation.
    """
    # template for all command codes
    #
    # @property
    # def COMMAND():
    #     """
    #     Example docstring.
    #     """
    #     return bytes([0])

    @property
    def SE():
        """
        End of subnegotiation parameters.
        """
        return bytes([240])

    @property
    def NOP():
        """
        No operation.
        """
        return bytes([241])

    @property
    def DM():
        """
        Data mark. Indicates the position of a Sync event within the data stream.
        This should always be accompanied by a TCP urgent notification.
        """
        return bytes([242])

    @property
    def BRK():
        """
        Break. Indicates the "break" or "attention" key was hit.
        """
        return bytes([243])

    @property
    def IP():
        """
        Suspend, interrupt or abort the process to which the NVT is connected.
        """
        return bytes([244])

    @property
    def AO():
        """
        Abort output. Allows the current process to run to completion but do not send
        its output to the user.
        """
        return bytes([245])

    @property
    def AYT():
        """
        Are you there? Send back to the NVT some visible evidence that the AYT was recieved.
        """
        return bytes([246])

    @property
    def EC():
        """
        Erase character. The reciever should delete the last preceding character from
        the data stream.
        """
        return bytes([247])

    @property
    def EL():
        """
        Erase line. Delete characters from the data stream back to but not including
        the previous CRLF (carriage return, line feed).
        """
        return bytes([248])

    @property
    def GA():
        """
        Go ahead. Used under certain circumstances, to tell the other end that it can transmit.
        """
        return bytes([249])

    @property
    def SB():
        """
        Subnegotiation of the indicated option follows.
        """
        return bytes([250])

    @property
    def WILL():
        """
        Indicates the desire to begin performing, or confirmation that you are
  	  	now performing, the indicated option.
        """
        return bytes([251])

    @property
    def WONT():
        """
        Indicates the refusal to perform, or continue performing, the indicated option.
        """
        return bytes([252])

    @property
    def DO():
        """
        Indicates the request that the other party perforn, or confirmation that you are
        expecting the other party to perform, the indicated option.
        """
        return bytes([253])

    @property
    def DONT():
        """
        Indicates the demand that the other party stop performing, or confirmation that you
  	  	are no longer expecting the other party to perform, the indicated option.
        """
        return bytes([254])

    @property
    def IAC():
        """
        Interpret as command.
        """
        return bytes([255])