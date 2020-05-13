#!/usr/bin/env python3.7

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import subprocess

import telepot

import utils

async def execute(bot, msg, chat_id, args, username):

    (rc, stdout, stderr) = await utils.execute_shell_command("uname -a")
    msg = stdout + '\n'

    (rc, stdout, stderr) = await utils.execute_shell_command(
                                    "cat /sys/class/thermal/thermal_zone0/temp")
    cpu_temp = str(float(stdout)/1000.0)
    msg += "CPU Temperature = " + cpu_temp + "ºC\n"

    (rc, stdout, stderr) = await utils.execute_shell_command(
                                    "/opt/vc/bin/vcgencmd measure_temp")
    gpu_temp = stdout.split("=")[1][0:-3]
    msg += "GPU Temperature = " + gpu_temp + "ºC\n\n"

    (rc, stdout, stderr) = await utils.execute_shell_command(
                                    "free -h | tail -n 2")
    mem = stdout.split()
    msg += "Available RAM = " + mem[6] + " / " + mem[1] + "\n\n"

    (rc, stdout, stderr) = await utils.execute_shell_command(
                                    "df -h / | tail -n 1")
    mem = stdout.split()
    msg += "Free SD = " + mem[3] + " / " + mem[1]

    await bot.sendMessage(chat_id, msg)
