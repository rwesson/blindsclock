#!/usr/bin/python

# test file to run service that doesn't yet interact at all with the main program

import threading
import time

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

CLIENT = OSCClient('localhost', 3002)

def ping(*_):
    'answer to ping messages'
    CLIENT.send_message(
        b'/message',
        [
            ''.join(sample(ascii_letters, randint(10, 20)))
            .encode('utf8'),
        ],
    )

def timer():
    global msg
    while True:
        print("yeah we notifying %d"%msg)
        msg+=1
        time.sleep(3)

def send_date():
    'send date to the application'
    CLIENT.send_message(
        b'/date',
        [asctime(localtime()).encode('utf8'), ],
    )


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    SERVER.bind(b'/ping', ping)
    while True:
        time.sleep(1)
        send_date()
