#!/usr/bin/env python3
import sys

from telethon import TelegramClient
from telethon.utils import get_display_name
from telethon.tl.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateShortMessage, UpdateShortChatMessage
)


TERMGRAM_VERSION = 0.1
API_ID = 
API_HASH = ''

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
        phone = input("Phone number: ")
        client.sign_in(phone=phone)
        code = input("Activation code: ")
        client.sign_in(code=code)
        if not client.is_user_authorized():
            print("Failed to authenticate. Try again.\n")


def loop():
    while True:
        try:
            if not current_chatroom:
                select_chatroom()
            active_chatroom()
        except KeyboardInterrupt:
            current_chatroom = None
            print('\n')
            select_chatroom()


def select_chatroom():
    try:
        options = {}
        option_count = 0
        dialogs, entities = client.get_dialogs(10)
        for entity in entities:
            label = get_display_name(entity)
            options[option_count] = entity
            print("{:>3}: {}".format(option_count, label))
            option_count += 1
        answer = int(input("\nSelect chatroom: "))
        global current_chatroom
        current_chatroom = options[answer]
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


def active_chatroom():
    while True:
        input('')


def update_handler(update):
    if isinstance(update, (UpdateNewMessage, UpdateNewChannelMessage)):
        if update.message.from_id == current_chatroom.id:
            date = str(update.message.date).split()[1][:-3]  # HH:MM
            sender = get_display_name(client.get_entity(update.message.from_id))
            message = update.message.message
            if not message:
                message = '{multimedia}'
            print("[{}] {}: {}".format(date, sender, message))

    elif isinstance(update, UpdateShortMessage, UpdateShortChatMessage):
        if update.chat_id == current_chatroom.id:
            date = str(update.date).split()[1][:-3]  # HH:MM
            sender = get_display_name(client.get_entity(update.from_id))
            message = update.message
            if not message:
                message = '{multimedia}'
            print("[{}] {}: {}".format(date, sender, message))


def main():
    init()
    welcome()
    login()
    loop()


if __name__ == '__main__':
    main()
