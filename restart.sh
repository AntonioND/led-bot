#/bin/bash

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

# This script must run as root

killall python3.7

# Set this path to the right location
cd /home/pi/led-bot

nohup ./led_server.py &

# Comment the following lines if you don't want to use the Telegram bot
cd telegram
nohup sudo -u pi ./run.py &
cd ..

# Comment the following lines if you don't want to use the HTML sever
cd webserver
nohup ./run.py &
