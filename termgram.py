#!/usr/bin/env python3
import sys

import urwid
from telethon import TelegramClient


API_ID = 
API_HASH = ''


def main():
    client = TelegramClient('termgram', API_ID, API_HASH)
    client.connect()
    if not client.is_user_authorized():
        phone = input("Phone number: ")
        client.sign_in(phone=phone)
        code = input("Activation code: ")
        client.sign_in(code=code)
        if not client.is_user_authorized():
            print("Invalid code. Try again.")
            sys.exit(1)


if __name__ == '__main__':
    main()
