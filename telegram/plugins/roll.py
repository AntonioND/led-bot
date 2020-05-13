#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import random

import telepot

async def execute(bot, msg, chat_id, args, username):

    if args == "help":
        await bot.sendMessage(chat_id,
                "/roll: Number from 0.0 to 1.0\n" +
                "/roll <max>: Number from 1 to <max>\n" +
                "/roll <min> <max>: Number from <min> to <max>")
        return

    try:
        _min = 1
        _max = 1

        args = args.split(' ')
        if len(args) == 1:
            _max = int(args[0])
        elif len(args) == 2:
            _min = int(args[0])
            _max = int(args[1])
        else:
            await bot.sendMessage(chat_id, "Too many arguments.")

        await bot.sendMessage(chat_id, str(random.randint(_min, _max)))

    except:
        await bot.sendMessage(chat_id, str(random.random()))
