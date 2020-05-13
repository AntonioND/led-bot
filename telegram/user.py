#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import os
import shutil
import sys

import telepot

import secrets
import utils

# Functions

def get_name(user_id):
    try:
        f = open('./ids/' + str(user_id), 'r')
        name = f.readline()
        name = name.strip()
        return name
    except:
        return None


def get_id(user_name):
    try:
        files = [f for f in os.listdir('./ids/')]
        for _file in files:
            if os.path.isfile(os.path.join('./ids/', _file)):
                f = open(os.path.join('./ids/', _file))
                name = f.readline()
                name = name.strip()
                if name == user_name: 
                    return _file 
        return None
    except:
        return None


def pass_correct(username, password):

    if not username.isalpha():
        return False

    try:
        f = open('./users/' + str(username) + "/pass", 'r')
        p = f.readline()
        f.close()
        p = p.strip()
        if p == password:
            return True
    except:
        return False

    return False


def has_permission(username, perm_name):

    if not username.isalpha():
        return False

    try:
        f = open('./users/' + str(username) + "/perm", 'r')
        perms = f.readlines()
        f.close()
        perms = [x[:-1] for x in perms]  # Remove newline
        if 'all' in perms:
            return True
        elif perm_name in perms:
            return True
    except:
        return False

    return False


# Returns None if failed login, the username if successful
async def login(bot, args, chat_id, sender_id):
    try:
        username, pass_ = args.split(" ", 1)
        if ' ' in pass_:
            await bot.sendMessage(chat_id, "Incorrect login command.")
            return None

        if not username.isalpha():
            await bot.sendMessage(chat_id, "Invalid user name.")
            return None

        if pass_correct(username, pass_):
            f = open('ids/' + str(sender_id), 'w')
            f.write(username)
            f.close()
            await bot.sendMessage(chat_id, "Logged in with user " + username +
                                  ".")
            return username
        else:
            await bot.sendMessage(chat_id, "Wrong credentials.")
            return None

    except:
        await bot.sendMessage(chat_id, "Failed to log in.")

    return None


async def logout(bot, args, chat_id, sender_id):
    try:
        username = get_name(sender_id)
        os.remove('ids/' + str(sender_id))
        await bot.sendMessage(chat_id, "User " + username + " logged out.")
        await bot.sendMessage(secrets.MY_USER_ID, "EVENT: User " + username +
                              " logged out.")
    except:
        await bot.sendMessage(chat_id, "Failed to log out.")


async def remove(bot, args, chat_id):

    args = args.split(" ")
    if len(args) != 2:
        await bot.sendMessage(chat_id, "Invalid remove command.")
        return

    username = args[1]

    if username == secrets.MY_USERNAME:
        await bot.sendMessage(chat_id, "Can't remove that user.")
        return

    if not username.isalpha():
        await bot.sendMessage(chat_id, "Invalid user name.")
        return None

    folderpath = 'users/' + username

    if not os.path.exists(folderpath):
        await bot.sendMessage(chat_id, "User doesn't exist.")
        return

    try:
        shutil.rmtree(folderpath, ignore_errors=True)
        await bot.sendMessage(chat_id, "User removed.")
    except:
        await bot.sendMessage(chat_id, "Failed to remove user.")


async def create(bot, args, chat_id):

    args = args.split(" ")
    if len(args) != 3:
        await bot.sendMessage(chat_id, "Invalid create command.")
        return

    username = args[1]

    folderpath = 'users/' + username

    if os.path.exists(folderpath):
        await bot.sendMessage(chat_id, "User already exist.")
        return

    if not username.isalpha():
        await bot.sendMessage(chat_id, "Invalid user name.")
        return None

    try:
        os.mkdir(folderpath)

        f = open(folderpath + "/pass", "w")
        f.write(args[2])
        f.close()

        f = open(folderpath + "/perm", "w")
        # Default permissions
        f.write("msg\n"
                "plugin\n"
                "rev\n"
                "roll\n"
                "sysinfo\n"
                "time\n"
                "whoami\n"
        )
        f.close()

        await bot.sendMessage(chat_id, "User created.")
    except:
        shutil.rmtree(folderpath, ignore_errors=True)
        await bot.sendMessage(chat_id, "Failed to create user.")

    return


async def add_permission(bot, args, chat_id):

    args = args.split(" ")
    if len(args) != 3:
        await bot.sendMessage(chat_id, "Invalid add permission command.")
        return

    username = args[1]

    folderpath = 'users/' + username

    if username == "skylyrac":
        await bot.sendMessage(chat_id, "Can't remove that user.")
        return

    if not os.path.exists(folderpath):
        await bot.sendMessage(chat_id, "User doesn't exist.")
        return

    try:
        f = open(folderpath + "/perm", "r")
        lines = f.readlines()
        f.close()

        teststr = args[2] + "\n"
        if teststr in lines:
            await bot.sendMessage(chat_id, "Permission already granted.")
            return

        f = open(folderpath + "/perm", "a")
        f.write(args[2] + "\n")
        f.close()

        await bot.sendMessage(chat_id, "Permission added.")
    except:
        await bot.sendMessage(chat_id, "Error while adding permission.")

    try:
        f = open(folderpath + "/perm", "r")
        lines = ''.join(f.readlines())
        f.close()
        await utils.send_message(bot, chat_id, lines)
    except:
        await bot.sendMessage(chat_id, "List permissions failed.")

    return


async def remove_permission(bot, args, chat_id):

    args = args.split(" ")
    if len(args) != 3:
        await bot.sendMessage(chat_id, "Invalid remove permission command.")
        return

    username = args[1]

    folderpath = 'users/' + username

    if not os.path.exists(folderpath):
        await bot.sendMessage(chat_id, "User doesn't exist.")
        return

    if not username.isalpha():
        await bot.sendMessage(chat_id, "Invalid user name.")
        return None

    try:
        f = open(folderpath + "/perm", "r")
        lines = f.readlines()
        f.close()

        f = open(folderpath + "/perm", "w")
        for l in lines:
            if l.strip() != args[2]:
                f.write(l)
        f.close()

        await bot.sendMessage(chat_id, "Permission removed.")
    except:
        await bot.sendMessage(chat_id, "Error while removing permission.")

    try:
        f = open(folderpath + "/perm", "r")
        lines = ''.join(f.readlines())
        f.close()
        await utils.send_message(bot, chat_id, lines)
    except:
        await bot.sendMessage(chat_id, "List permissions failed.")

    return


async def list_permission(bot, args, chat_id):

    args = args.split(" ")
    if len(args) != 2:
        await bot.sendMessage(chat_id, "Invalid list permission command.")
        return

    username = args[1]

    folderpath = 'users/' + username

    if not os.path.exists(folderpath):
        await bot.sendMessage(chat_id, "User doesn't exist.")
        return

    if not username.isalpha():
        await bot.sendMessage(chat_id, "Invalid user name.")
        return None

    try:
        f = open(folderpath + "/perm", "r")
        lines = ''.join(f.readlines())
        f.close()
        await utils.send_message(bot, chat_id, lines)
    except:
        await bot.sendMessage(chat_id, "List permissions failed.")

    return


async def set_password(bot, args, chat_id):

    args = args.split(" ")
    if len(args) != 3:
        await bot.sendMessage(chat_id, "Invalid set password command.")
        return

    username = args[1]

    folderpath = 'users/' + username

    if not os.path.exists(folderpath):
        await bot.sendMessage(chat_id, "User doesn't exist.")
        return

    if not username.isalpha():
        await bot.sendMessage(chat_id, "Invalid user name.")
        return None

    try:
        f = open(folderpath + "/pass", "w")
        f.write(args[2])
        f.close()

        await bot.sendMessage(chat_id, "Password changed successfully.")
    except:
        await bot.sendMessage(chat_id, "Failed to change password.")

    return
