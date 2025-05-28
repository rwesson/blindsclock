from random import sample, randint
from string import ascii_letters
from time import sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

CLIENT = OSCClient('0.0.0.0', 3002)


def ping(*_):
    print("ping")
    CLIENT.send_message(
        b'/message',
        [
            ''.join(sample(ascii_letters, randint(10, 20)))
            .encode('utf8'),
        ],
    )


def call_update():
    print("sending update trigger")
    CLIENT.send_message(
        b'/date',
        [b"update"],
    )


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('0.0.0.0', port=3000, default=True)
    SERVER.bind(b'/ping', ping)
    while True:
        sleep(1)
        call_update()
