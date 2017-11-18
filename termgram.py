#!/usr/bin/env python3
import sys

from telethon import TelegramClient
from telethon.utils import get_display_name
from telethon.tl.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateShortMessage, UpdateShortChatMessage
)


TERMGRAM_VERSION = 0.1
API_ID = 117120
API_HASH = '4f3d31306935d48f1c9cc42b75838521'

client = TelegramClient('termgram', API_ID, API_HASH, update_workers=1)
current_chatroom = None  # User or Group you're chatting


def init():
    client.add_update_handler(update_handler)


def welcome():
    t = '''
         _ 
        | |
        | |_ ___ _ __ _ __ ___   __ _ _ __ __ _ _ __ ___  
        | __/ _ \ '__| '_ ` _ \ / _` | '__/ _` | '_ ` _ \ 
        | ||  __/ |  | | | | | | (_| | | | (_| | | | | | |
         \__\___|_|  |_| |_| |_|\__, |_|  \__,_|_| |_| |_|
                                 __/ |
                                |___/   v{}              
        '''
    print(t.format(TERMGRAM_VERSION))


def login():
    client.connect()
    while not client.is_user_authorized():
        try:
            phone = input("Phone number: ")
            client.sign_in(phone=phone)
            code = input("Activation code: ")
            client.sign_in(code=code)
            if not client.is_user_authorized():
                print("Failed to authenticate. Try again.\n")
        except KeyboardInterrupt:
            sys.exit(0)


def loop():
    while True:
        try:
            if not current_chatroom:
                select_chatroom()
            active_chatroom()
        except KeyboardInterrupt:
            global current_chatroom
            current_chatroom = None
            print('\n')
            select_chatroom()


def select_chatroom():
    try:
        options = {}
        option_count = 0
        dialogs, entities = client.get_dialogs(15)
        for entity in entities:
            label = get_display_name(entity)
            options[option_count] = entity
            print("{:>3}: {}".format(option_count, label))
            option_count += 1
        answer = int(input("\nSelect chatroom: "))
        global current_chatroom
        current_chatroom = options[answer]
    except KeyboardInterrupt:
        sys.exit(0)


def active_chatroom():
    while True:
        msg = input('')
        client.send_message(current_chatroom, msg)


def display_message(date, sender_id, message):
    date = date.strftime("%H:%M")
    sender_name = get_display_name(client.get_entity(sender_id))
    if not message:
        message = '{multimedia}'
    print("[{}] {}: {}".format(date, sender_name, message))


def update_handler(update):
    if isinstance(update, (UpdateNewMessage, UpdateNewChannelMessage)):
        if update.message.from_id == current_chatroom.id:
            display_message(update.message.date, update.message.from_id, update.message.message)

    elif isinstance(update, UpdateShortMessage):
        if update.user_id == current_chatroom.id:
            display_message(update.date, update.user_id, update.message)

    elif isinstance(update, UpdateShortChatMessage):
        if update.chat_id == current_chatroom.id:
            display_message(update.date, update.from_id, update.message)


def main():
    init()
    welcome()
    login()
    loop()


if __name__ == '__main__':
    main()
