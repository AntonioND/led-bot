#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import telepot

async def execute(bot, msg, chat_id, args, username):

    sender_id = msg['from']['id']

    first_name = None
    last_name = None
    sender_name = "<Undefined>"

    try:
        first_name = msg['from']['first_name']
    except:
        pass

    try:
        last_name = msg['from']['last_name']
    except:
        pass

    if first_name != None and last_name == None:
        sender_name = first_name
    elif first_name == None and last_name != None:
        sender_name = last_name
    elif first_name != None and last_name != None:
        sender_name = first_name + ' ' + last_name

    msg = ("Hello, " + sender_name + ". Your user ID is " +
          str(sender_id) + ". You're logged in as user " +
          username + ".")

    if chat_id != sender_id:
        msg += " The ID of this chat is: " + str(chat_id)

    await bot.sendMessage(chat_id, msg)
