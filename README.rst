Smart LED lamp (Raspberry Pi + Unicorn HAT)
===========================================

This repository contains a Telegram bot and a HTML server that can be used to
remotely control the lights of a `Unicorn HAT`_ connected to a Raspberry Pi.

This is a video that shows it in action:

https://www.youtube.com/watch?v=xjQCvFdkGJw

Both the Telegram bot and the HTML server can control the lights and don't need
the other one. If you don't want one of them, edit the file ``restart.sh`` to
remove the one you don't need.

In order to run the code in this repository, you need to install the following
dependencies:

.. code:: bash

    sudo apt install python3-pip python3-dev
    sudo pip3 install unicornhat

There are 3 main parts:

- **LED server**: Script that has to be run with root permissions. It listens to
  connections to a specific port and affects the LEDs. It can also reboot or
  shutdown your Raspberry Pi.

- **Telegram bot**: Telegram bot that runs with regular user permissions. It can
  send commands to the LED server.

- **HTML server**: HTML server that sets up a website with some buttons that can
  be used to control the LEDs. It sends commands to the LED server.

Note that you don't need the Telegram bot and HTML server at the same time. Just
one is enough. Also, any program that connects to the right port can send the
same commands to the LED server.

Start scripts
-------------

Open ``restart.sh`` and edit as needed following the instructions. You can
choose to disable specific modules, and you have to set the right path to the
code in your case. Note that this script must run as root.

HTML server
-----------

The dependency needed for the server is `Flask`_:

.. code:: bash

    pip3 install flask

The server runs on port 5000. All you need to do to open the website is to know
the IP address of your Raspberry Pi (with ``hostname -I``, for example). Then,
supposing that your IP address is 192.168.1.42, open your web browser and go to
``http://192.168.1.42:5000``.

Telegram bot
------------

The dependency needed for the server is `Telepot`_. Unfortunately, this library
is now discontinued, but I created this bot back when it was being maintained.
Eventually it will probably stop working.

.. code:: bash

    pip3 install telepot

You need to follow the instructions here to create your own Telegram bot and
`get a token`_.

You also need to edit the file ``telegram/secrets.py``:

.. code:: python

    MY_USERNAME = 'sampleroot'
    MY_USER_ID = 12345678
    TOKEN = '123456789:ABCDEFGHIJ-abcdefghijklmnopqrstuvwx'

The values are:

- ``MY_USERNAME``: Name of the username that acts as owner of the bot
- ``MY_USER_ID``: Telegram user ID. You can use the bot @userinfobot to get it.
- ``TOKEN``: Token obtained in the link above.

Rename the folder ``telegram/users/sampleroot`` to your chosen user name. Then,
edit the file ``pass`` inside it. Yes, it is plain text.

Now, open a chat window with your bot, and do ``/user login sampleroot pass``.
You can send commands to the LED server with commands such ``/led rainbow``. You
can try ``/led help`` for more information.

Start at boot
-------------

You can also edit your ``/etc/crontab`` file (you need root permissions) if
you want to run the scripts at boot automatically. Just add the following
lines at the end (replacing the path by the right one in your case):

.. code:: bash

    # Restart LED scripts every day at 11:00 A.M.
    0 11    * * *   root    /home/pi/led-bot/restart.sh

    # Start LED scripts at boot
    @reboot         root    /home/pi/led-bot/restart.sh

Contact
-------

You can contact me at antonio_nd at outlook com.

Website: http://www.skylyrac.net/

GitHub: https://github.com/AntonioND

Copyright (c) 2020, Antonio Niño Díaz

.. _Unicorn HAT: https://github.com/pimoroni/unicorn-hat
.. _Flask: https://flask.palletsprojects.com/
.. _Telepot: https://github.com/nickoala/telepot
.. _get a token: https://telepot.readthedocs.io/en/latest/#id5
