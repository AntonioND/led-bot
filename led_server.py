#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import colorsys
import math
import os
import select
import socket
import sys
import time

from random import randint, uniform

import unicornhat as unicorn

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Initialize LEDs

width = 0
height = 0

def reset_leds():
    global width, height
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(1.0)
    width, height= unicorn.get_shape()

reset_leds()

# Initialize server

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Listening on port " + str(PORT))

CURRENT_MODE = b''

read_list = [server_socket]

i = 0.0
h = 0.0
speed_multiplier = 1.0

while True:

    # Check server status

    readable, writable, errored = select.select(read_list, [], [], 0)
    for s in readable:
        if s is server_socket:
            client_socket, address = server_socket.accept()
            read_list.append(client_socket)
            print("Connection from" + str(address))
        else:
            data = s.recv(64)
            if data:
                print(data)
                if data == b'slow':
                    speed_multiplier = 0.25
                elif data == b'normal':
                    speed_multiplier = 1.0
                else:
                    CURRENT_MODE = data
                    reset_leds()
            else:
                s.close()
                read_list.remove(s)

    # Update LEDs

    if CURRENT_MODE == b'rainbow':
        i = i + 0.3 * speed_multiplier
        offset = 30
        for y in range(height):
            for x in range(width):
                r = (math.cos((x + i) / 2.0) + math.cos((y + i) / 2.0)) * 64.0 + 128.0
                g = (math.sin((x + i) / 1.5) + math.sin((y + i) / 2.0)) * 64.0 + 128.0
                b = (math.sin((x + i) / 2.0) + math.cos((y + i) / 1.5)) * 64.0 + 128.0
                r = max(0, min(255, r + offset))
                g = max(0, min(255, g + offset))
                b = max(0, min(255, b + offset))
                unicorn.set_pixel(x, y, int(r), int(g), int(b))
        unicorn.show()
    elif CURRENT_MODE == b'hue':
        i = i + 0.1 * speed_multiplier
        h = h + 0.001 * speed_multiplier
        for y in range(height):
            for x in range(width):
                v = math.cos((x + y + i) / 4.0) * 0.25 + 0.75
                (r, g, b) = colorsys.hsv_to_rgb(h, 1.0, v)
                #v = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                #r = v * math.sin(h + (((2 * math.pi) / 3) * 1))
                #g = v * math.sin(h + (((2 * math.pi) / 3) * 2))
                #b = v * math.sin(h + (((2 * math.pi) / 3) * 3))
                r = max(0, min(255, r * 255))
                g = max(0, min(255, g * 255))
                b = max(0, min(255, b * 255))
                unicorn.set_pixel(x, y, int(r), int(g), int(b))
        unicorn.show()
    elif CURRENT_MODE == b'red':
        i = i + 0.1 * speed_multiplier
        for y in range(height):
            for x in range(width):
                r = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                r = max(0, min(255, r))
                unicorn.set_pixel(x, y, int(r), 0, 0)
        unicorn.show()
    elif CURRENT_MODE == b'green':
        i = i + 0.1 * speed_multiplier
        for y in range(height):
            for x in range(width):
                g = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                g = max(0, min(255, g))
                unicorn.set_pixel(x, y, 0, int(g), 0)
        unicorn.show()
    elif CURRENT_MODE == b'blue':
        i = i + 0.1 * speed_multiplier
        for y in range(height):
            for x in range(width):
                b = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                b = max(0, min(255, b))
                unicorn.set_pixel(x, y, 0, 0, int(b))
        unicorn.show()
    elif CURRENT_MODE == b'yellow':
        i = i + 0.1 * speed_multiplier
        for y in range(height):
            for x in range(width):
                v = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                v = max(0, min(255, v))
                unicorn.set_pixel(x, y, int(v), int(v), 0)
        unicorn.show()
    elif CURRENT_MODE == b'cyan':
        i = i + 0.1 * speed_multiplier
        for y in range(height):
            for x in range(width):
                v = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                v = max(0, min(255, v))
                unicorn.set_pixel(x, y, 0, int(v), int(v))
        unicorn.show()
    elif CURRENT_MODE == b'magenta':
        i = i + 0.1 * speed_multiplier
        for y in range(height):
            for x in range(width):
                v = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                v = max(0, min(255, v))
                unicorn.set_pixel(x, y, int(v), 0, int(v))
        unicorn.show()
    elif CURRENT_MODE == b'white':
        i = i + 0.1 * speed_multiplier
        for y in range(height):
            for x in range(width):
                v = math.cos((x + y + i) / 4.0) * 64.0 + 192.0
                v = max(0, min(255, v))
                unicorn.set_pixel(x, y, int(v), int(v), int(v))
        unicorn.show()
    elif CURRENT_MODE == b'fire':
        if i > 3:
            i = 0;
        else:
            i = i + 1

        if i == 0:
            for y in range(0, height):
                for x in range(0, width):
                    low_step = max((height - y - 1.2) / height, 0)
                    mid_step = max((height - y - 1) / height, 0)
                    high_step = max((height - y) / height, 0)

                    x_center = 1.0 - abs(((width / 2) - x - 0.5) / (width / 2))

                    v = uniform(mid_step, high_step)

                    r = v * math.sqrt(math.sqrt(x_center))
                    g = v * low_step * x_center

                    r = int(r * 255)
                    g = int(g * 255)
                    b = int(0)
                    unicorn.set_pixel(x, y, r, g, b)
            unicorn.show()
    elif CURRENT_MODE == b'sparkles':
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
    elif CURRENT_MODE == b'reboot':
        for y in range(height):
            for x in range(width):
                unicorn.set_pixel(x, y, 0, 0, 0)
        unicorn.show()
        os.system('sudo reboot')
    elif CURRENT_MODE == b'shutdown':
        for y in range(height):
            for x in range(width):
                unicorn.set_pixel(x, y, 0, 0, 0)
        unicorn.show()
        os.system('sudo shutdown now')
    else:
        for y in range(height):
            for x in range(width):
                unicorn.set_pixel(x, y, 0, 0, 0)
        unicorn.show()

    time.sleep(0.01)

sys.exit(0)
