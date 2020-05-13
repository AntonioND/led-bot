#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import asyncio
import importlib
import os
import re
import subprocess
import sys
import textwrap
import time

import telepot
import telepot.aio

import secrets
import user
import utils

# Constants

PLUGIN_FOLDER = 'plugins'

# Global variables

BOT = 0
PLUGIN_LIST = []
PLUGIN_LIST_NAMES = []

# Functions

def plugin_reload_all():
    global PLUGIN_LIST
    global PLUGIN_LIST_NAMES

    importlib.invalidate_caches()
    pysearchre = re.compile('.py$', re.IGNORECASE)
    pluginfiles = filter(pysearchre.search,
                         os.listdir(os.path.join(os.path.dirname(__file__),
                                    PLUGIN_FOLDER)))
    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = map(form_module, pluginfiles)
    # import parent module / namespace
    importlib.import_module(PLUGIN_FOLDER)
    PLUGIN_LIST = []
    PLUGIN_LIST_NAMES = []
    for plugin in plugins:
        if not plugin.startswith('__'):
            PLUGIN_LIST_NAMES.append(plugin[1:])
            this_plugin = importlib.import_module(plugin, package=PLUGIN_FOLDER)
            PLUGIN_LIST.append(this_plugin)
            # Run init() function of each plugin (if it exists)
            try:
                method_to_call = getattr(this_plugin, 'init')
                method_to_call()
            except:
                pass


async def execute_bot_command_line(bot, msg, chat_id, cmdline):

    cmd = cmdline
    args = ""

    if ' ' in cmdline:
        cmd, args = cmdline.split(" ", 1)

    sender_id = msg['from']['id']

    # Get user name of whoever sent the text

    sender_name = user.get_name(sender_id)

    # If the sender hasn't logged in, don't allow anything else but login

    if sender_name == None:

        if cmd == "login":

            username = await user.login(bot, args, chat_id, sender_id)

            first_name = None
            last_name = None
            name = "<Undefined>"

            try:
                first_name = msg['from']['first_name']
            except:
                pass

            try:
                name = msg['from']['last_name']
            except:
                pass

            if first_name != None and last_name == None:
                name = first_name
            elif first_name == None and last_name != None:
                name = last_name
            elif first_name != None and last_name != None:
                name = first_name + ' ' + last_name

            chat_info_str = ""
            if sender_id != chat_id:
                chat_info_str += "Sender ID " + str(sender_id) + ". "
            chat_info_str += "Chat ID " + str(chat_id) + ". Name [" + name + "]"

            if username != None:
                status = "Successful"
                # Tell me about the new login
                await bot.sendMessage(secrets.MY_USER_ID,
                        "EVENT: Login of user " + username + ". " + chat_info_str)
            else:
                # Tell me about the failed login
                await utils.send_message(bot, secrets.MY_USER_ID,
                        "EVENT: Failed login [" + args + "]. " + chat_info_str)

        else:
            await bot.sendMessage(chat_id, "Please, log in.\n" +
                                           "/login <username> <password>")

        return

    if cmd == "login":
        username = user.get_name(sender_id)
        await bot.sendMessage(chat_id, "Already logged in as " + username + ".")
        return

    elif cmd == "logout":
        await user.logout(bot, args, chat_id, sender_id)
        return

    elif cmd == "help":
        plugins = "/" + "\n/".join(PLUGIN_LIST_NAMES)
        await bot.sendMessage(chat_id,
                "/login <username> <password>\n" +
                "/logout\n" +
                "/user\n" +
                "/plugin\n" +
                "/cmd\n" +
                plugins)
        return


    # Only continue if user has permission to do this, but don't tell the user
    # about the lack of permission.

    if not user.has_permission(sender_name, cmd):
        await bot.sendMessage(chat_id, "Command not available.")
        return

    # First, check all internal commands. Then, check plugins.

    if cmd == "user":

        if sender_id != secrets.MY_USER_ID:
            await bot.sendMessage(chat_id, "You have no permission to do that.")
            return

        if args.startswith("new "):
            await user.create(bot, args, chat_id)
            return

        elif args.startswith("remove "):
            await user.remove(bot, args, chat_id)
            return

        elif args.startswith("setpass "):
            await user.set_password(bot, args, chat_id)
            return

        elif args.startswith("addperm "):
            await user.add_permission(bot, args, chat_id)
            return

        elif args.startswith("removeperm "):
            await user.remove_permission(bot, args, chat_id)
            return

        elif args.startswith("listperm "):
            await user.list_permission(bot, args, chat_id)
            return

        elif args == "help":
            await bot.sendMessage(chat_id,
                    "/user new <name> <pass>: Create user\n" +
                    "/user remove <name>: Remove user\n" +
                    "/user setpass <name> <pass>: Change password\n" +
                    "/user addperm <name> <perm>: Add permission\n" +
                    "/user removeperm <name> <perm>: Remove permission\n" +
                    "/user listperm <name> <perm>: List permissions")
            return

    elif cmd == "plugin":

        if args == "reload":

            if sender_id != secrets.MY_USER_ID:
                await bot.sendMessage(chat_id, "You have no permission to do that.")
                return

            plugin_reload_all()
            await bot.sendMessage(chat_id, "Loaded plugins: " +
                            ' '.join(PLUGIN_LIST_NAMES))
            return
        elif args == "list":
            await bot.sendMessage(chat_id, "Available plugins: " +
                            ' '.join(PLUGIN_LIST_NAMES))
            return
        elif args == "help":
            await bot.sendMessage(chat_id,
                    "/plugin reload: Reload plugins.\n" +
                    "/plugin list: List available plugins.")
            return

    elif cmd == "cmd":

        if sender_id != secrets.MY_USER_ID:
            await bot.sendMessage(chat_id, "You have no permission to do that.")
            return

        shell_cmd = args

        if len(shell_cmd) > 0:
            (rc, stdout, stderr) = await utils.execute_shell_command(shell_cmd)
            if rc != None:
                if rc != 0 or ((len(stdout) == 0) and (len(stderr) == 0)):
                    await utils.send_message(bot, chat_id, "rc = " + str(rc))
                if len(stdout) > 0:
                    await utils.send_message(bot, chat_id, stdout)
                if len(stderr) > 0:
                    await utils.send_message(bot, chat_id, "stderr")
                    await utils.send_message(bot, chat_id, stderr)
        else:
            await bot.sendMessage(chat_id, "No command for shell found.")
        return

    elif cmd in PLUGIN_LIST_NAMES:
        index = PLUGIN_LIST_NAMES.index(cmd)
        try:
            method_to_call = getattr(PLUGIN_LIST[index], 'execute')
            await method_to_call(bot, msg, chat_id, args, sender_name)
        except:
            await utils.send_message(bot, chat_id,
                    "Plugin command exception:\n" +
                    textwrap.indent(str(sys.exc_info()[0]),"      ") + "\n" +
                    textwrap.indent(str(sys.exc_info()[1]),"      "))
        return

    await bot.sendMessage(chat_id, "Command not found.")
    return


async def message_handle(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type != 'text':
        return

    command = msg['text']

    if command[0] == '/':
        command = command[1:]
    else:
        return # Not a command

    try:
        await execute_bot_command_line(BOT, msg, chat_id, command)
    except:
        await utils.send_message(BOT, chat_id, "message_handle():\n" +
                textwrap.indent(str(sys.exc_info()[0]),"      ") + "\n" +
                textwrap.indent(str(sys.exc_info()[1]),"      "))


def main():

    global BOT

    print("SkyLyrac's Home Bot")
    print("-------------------")

    print("")

    plugin_reload_all()

    print("Plugins: " + ' '.join(PLUGIN_LIST_NAMES))

    print("")

    BOT = telepot.aio.Bot(secrets.TOKEN)

    #print("Bot Info: " + str(BOT.getMe())))

    #print("")

    loop = asyncio.get_event_loop()

    print('Listening to messages...')

    loop.create_task(BOT.message_loop(message_handle))
    loop.run_forever()

# Run

if __name__ == "__main__":
    #try:
    main()
    #except:
    #    utils.send_message(BOT, chat_id, "main():\n" +
    #            textwrap.indent(str(sys.exc_info()[0]),"      ") + "\n" +
    #            textwrap.indent(str(sys.exc_info()[1]),"      "))
    #    os.exit(1)

