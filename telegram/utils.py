#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import subprocess
import telepot

# Constants

MAX_LENGHT = (4 * 1024)

# Functions

async def send_message(bot, chat_id, msg):

    while (len(msg) > MAX_LENGHT):
        send = msg[:MAX_LENGHT]
        msg = msg[MAX_LENGHT:]
        await bot.sendMessage(chat_id, send)

    if len(msg) > 0:
        await bot.sendMessage(chat_id, msg)


async def execute_shell_command(cmd_line):
    try:
        p = subprocess.Popen(cmd_line, stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE, shell = True)
        (stdout, stderr) = p.communicate()

        stdout = stdout.decode()
        stderr = stderr.decode()
    except:
        await utils.send_message(bot, chat_id, "execute_shell_command():\n" +
                textwrap.indent(str(sys.exc_info()[0]),"      ") + "\n" +
                textwrap.indent(str(sys.exc_info()[1]),"      "))
        return None

    return (p.returncode, stdout, stderr)
