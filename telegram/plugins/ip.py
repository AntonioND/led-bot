#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import subprocess

from requests import get

import telepot

import utils

async def execute(bot, msg, chat_id, args, username):

    public_ip = get('https://api.ipify.org').text

    (rc, stdout, stderr) = await utils.execute_shell_command("hostname -I")

    local_ip = stdout

    await bot.sendMessage(chat_id, "Public IP: " + public_ip + "\n" +
                                   "Local IP: " + local_ip)
