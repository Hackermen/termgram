#!/usr/bin/env python3
import datetime
import sys
import time

import urwid
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import User, Channel


API_ID = 
API_HASH = ''

client = TelegramClient('termgram', API_ID, API_HASH)
selected_chat = None


def login():
    client.connect()
    while not client.is_user_authorized():
        phone = input("Phone number: ")
        client.sign_in(phone=phone)
        code = input("Activation code: ")
        client.sign_in(code=code)
        if not client.is_user_authorized():
            print("Invalid code. Try again.\n")


def select_chatroom():
    options = {}
    option_count = 0
    dialogs, entities = client.get_dialogs(10)
    for entity in entities:
        if isinstance(entity, User):
            if entity.first_name:
                label = entity.first_name
            if entity.last_name:
                label += ' ' + entity.last_name
            if not label and entity.username:
                label = entity.username
            if not label:
                label = entity.id
        if isinstance(entity, Channel):
            label = entity.title
        option_count += 1
        options[option_count] = entity
        print("{:>3}: {}".format(option_count, label))
    answer = int(input("\nSelect chatroom: "))
    global selected_chat
    selected_chat = options[answer]


def open_chatroom():
    while True:
        result = client(GetHistoryRequest(
            selected_chat,
            limit=10,
            offset_date=datetime.datetime.now(),
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0
        ))
        for msg in reversed(result.messages):
            print(msg.message)
        time.sleep(3)


def main():
    login()
    select_chatroom()
    open_chatroom()


if __name__ == '__main__':
    main()
