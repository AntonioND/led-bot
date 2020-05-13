#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import telepot
import user

async def execute(bot, msg, chat_id, args, username):

    dest_name, msg = args.split(" ", 1)

    dest_id = user.get_id(dest_name)

    await bot.sendMessage(dest_id, username + ': ' + msg)
