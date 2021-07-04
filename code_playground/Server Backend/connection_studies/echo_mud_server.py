#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 13:39:29 2020

@author: AzureDVBB

Using TELNET for MUD client connections and https://docs.python.org/3/library/asyncio-stream.html
for the async connections.
"""

import asyncio
import socket

async def handle_connection(reader, writer):
    # NOTE: the MUD servers usually use the telnet protocol to communicate between server and client
    # for more information on commands and negotiation, search google for 'telnet command codes' or
    # visit https://users.cs.cf.ac.uk/Dave.Marshall/Internet/node141.html as I have used it as
    # a reference here
    addr = writer.get_extra_info('peername')
    print(f"!!!! New connection recived from: {addr}")

    ############# TELNET negotiations testing
    print(f"??<< Sending 'are_you_there' command {bytes([255, 253, 246])}")
    # NOTE: this sends a TELNET request to the connected client to check if they are still there
    # the first value '255' is 'interpret-as-command (IAC)' must precede all commands sent to
    # clients, next is the '253' or 'do-preform (DO)' command, indicating the client
    # should do this command and finally
    # '246' or 'are-you-there (AYT)' command requests a response from the client
    writer.write(bytes([255, 253, 246]))
    await writer.drain()
    ret = await reader.read(100)
    # Will return a response (with client tintin++ and mudlet)
    # b'\xff\xfc\xf6' decoded as [255, 252, 246]
    # that is, interpret-as-command, Won't perform , are-you-there, (IAC, WON'T, AYT)
    # this is basically just a ping to the client to check if they are still there
    print(f"??>> Recieved response {ret}")

    print("??<< Sending request for terminal type")
    # Sends a check to see if the client will perform the transaction, once again see
    # https://users.cs.cf.ac.uk/Dave.Marshall/Internet/node141.html where this example
    # has been taken from
    writer.write(bytes([255,253,24])) # IAC DO (terminal type)
    await writer.drain()
    ret = await reader.read(100)
    print(f"??>> Recieved response {ret}")
    if ret == b'\xff\xfb\x18': # client will do the negotiation
        print("  ?< Interpreted as WILL DO, sending command to identify terminal type..")
        writer.write(bytes([255, 250, 24, 1, 255, 240])) # IAC SB (termintal-type) (1) IAC SE
        await writer.drain()
        ret = await reader.read(100)
        # the response should be: 255 250 24 0 <list of characters here> 255 240
        # that is: IAC SB (terminal-type) (0) <list of characters here> IAC SE
        print(f"  ?> Recieved response {ret}")
        ttype = str(ret).split('\\')[-3][3:] # takes the list of characters returned (terminal type)
        print(f"  ?~ Terminal identity confirmed as {ttype}")
    else: # client will not do, or gave an unexpected response
        print("  ~~ Interpreted as WON'T DO, terminal type will remain a mystery.")

    ############## echo server loop
    while True:
        # NOTE: readline() will stop reading at b'\n'
        # This means that 'message\nbroken' sent by client is interpreted as two seperate commands
        # 'message\n' and 'broken\r\n'
        data = await reader.readline()
        if data == b'': # connection closed
            break

        message = data.decode()
        print(f">>>> Raw Message '{data}'")
        print(f"~~~~ Decoded message '{message.strip()}'")
        print("<<<< Echoing back original message...")
        writer.write(data)
        await writer.drain()
        print(f'++++ Echoed successfully. Awaiting new message..')

    print(f"XXXX Closing connection from {addr}")
    writer.close()


async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888,
                                        family=socket.AF_INET, flags=socket.AI_PASSIVE,
                                        reuse_address = 1, reuse_port = 1,
                                        ssl=None, ssl_handshake_timeout=None)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())