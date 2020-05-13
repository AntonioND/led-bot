#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020, Antonio Niño Díaz <antonio_nd@outlook.com>

import socket

from flask import Flask, render_template, request

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

app = Flask(__name__)

def send_command(command):
    command = str(command)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())

@app.route("/", methods=['GET', 'POST'])
def index():
    #print(request.method)

    if request.method == 'POST':

        commands = [
            'Off',
            'Rainbow', 'Hue', 'Sparkles',
            'Red', 'Green', 'Blue', 'Yellow', 'Cyan', 'Magenta', 'White',
            'Normal', 'Slow',
            'Reboot', 'Shutdown'
        ]

        valid = False
        for c in commands:
            if request.form.get(c) == c:
                send_command(c.lower())
                valid = True
         
        if not valid: # Unknown command
            return render_template("index.html")

    elif request.method == 'GET':
        pass

    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
