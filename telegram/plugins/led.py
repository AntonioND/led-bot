#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>


import socket

import telepot

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

async def execute(bot, msg, chat_id, args, username):

    try:
        command = str(args)

        if command == "help":
            await bot.sendMessage(chat_id,
                '/led off\n'
                '/led {rainbow,hue,sparkles}\n'
                '/led {red,green,blue,yellow,cyan,white}\n'
                '/led {normal,slow}\n'
                '/led {reboot,shutdown}'
            )

            return

        #await bot.sendMessage(chat_id, command)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(command.encode())

    except:
        await bot.sendMessage(chat_id, "Exception")
