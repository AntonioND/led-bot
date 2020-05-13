#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import telepot

async def execute(bot, msg, chat_id, args, username):

    await bot.sendMessage(chat_id, args[::-1])
