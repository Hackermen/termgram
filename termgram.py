#!/usr/bin/env python3
import datetime
import sys

import urwid
from telethon import TelegramClient
from telethon.utils import get_display_name
from telethon.tl import types


TERMGRAM_VERSION = 0.1
API_ID = 
API_HASH = ''

telegram = TelegramClient('termgram', API_ID, API_HASH, update_workers=1)
current_chat = None  # User or Group you're chatting

input_field = urwid.Edit('>: ')
messages_field = urwid.Text('')
mainframe = None  # urwid window
mainloop = None  # urwid loop


def init():
    telegram.add_update_handler(update_handler)

    global mainframe
    mainframe = urwid.LineBox(
        urwid.Pile([
            ('weight', 70, urwid.Filler(messages_field)),
            ('fixed', 1, urwid.Filler(input_field)),
        ]),
    )
    global mainloop
    mainloop = urwid.MainLoop(mainframe, unhandled_input=input_handler)


def welcome():
    t = '''
         _
        | |
        | |_ ___ _ __ _ __ ___   __ _ _ __ __ _ _ __ ___
        | __/ _ \ '__| '_ ` _ \ / _` | '__/ _` | '_ ` _ \\
        | ||  __/ |  | | | | | | (_| | | | (_| | | | | | |
         \__\___|_|  |_| |_| |_|\__, |_|  \__,_|_| |_| |_|
                                 __/ |
                                |___/   v{}
        '''
    print(t.format(TERMGRAM_VERSION))


def login():
    telegram.connect()
    while not telegram.is_user_authorized():
        try:
            phone = input("Phone number: ")
            telegram.sign_in(phone=phone)
            code = input("Activation code: ")
            telegram.sign_in(code=code)
            if not telegram.is_user_authorized():
                print("Failed to authenticate. Try again.\n")
        except KeyboardInterrupt:
            sys.exit(0)


def loop():
    global current_chat
    while True:
        try:
            if not current_chat:
                select_chatroom()
            active_chatroom()
        except KeyboardInterrupt:
            current_chat = None
            print('\n')
            select_chatroom()


def select_chatroom():
    try:
        options = {}
        option_count = 0
        dialogs, entities = telegram.get_dialogs(15)
        for entity in entities:
            label = get_display_name(entity)
            options[option_count] = entity
            print("{:>3}: {}".format(option_count, label))
            option_count += 1
        answer = int(input("\nSelect chatroom: "))
        global current_chat
        current_chat = options[answer]
    except KeyboardInterrupt:
        sys.exit(0)


def active_chatroom():
    mainloop.run()


def display_message(date, sender_id, message):
    date = date.strftime("%H:%M")
    sender_name = get_display_name(telegram.get_entity(sender_id))
    if not message:
        message = '{multimedia ¯\_(ツ)_/¯}'
    message = "[{}] {}: {}".format(date, sender_name, message)
    messages_field.set_text(messages_field.text + '\n' + message)
    mainloop.draw_screen()


def update_handler(update):
    if isinstance(update, (types.UpdateNewMessage, types.UpdateNewChannelMessage)):
        if update.message.from_id == current_chat.id or update.message.to_id.channel_id == current_chat.id:
            display_message(update.message.date, update.message.from_id, update.message.message)

    elif isinstance(update, types.UpdateShortMessage):
        if update.user_id == current_chat.id:
            display_message(update.date, update.user_id, update.message)

    elif isinstance(update, types.UpdateShortChatMessage):
        if update.chat_id == current_chat.id:
            display_message(update.date, update.from_id, update.message)


def input_handler(key):
    if key == 'enter':
        msg = input_field.get_edit_text()
        if msg.strip():  # not empty message
            telegram.send_message(current_chat, msg)
            display_message(datetime.datetime.now(), telegram.get_me(), msg)
            input_field.set_edit_text('')  # clear

    elif key == 'esc':
        # @TODO: select another chatroom?
        pass

    elif key == 'ctrl l':
        messages_field.set_text('')  # clear all messages
        mainloop.draw_screen()


def main():
    init()
    welcome()
    login()
    loop()


if __name__ == '__main__':
    main()
