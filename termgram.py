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
header_text = urwid.Text('termgram')
mainframe = None  # urwid.Frame
mainloop = None  # urwid.MainLoop
message_list = None  # urwid.ListBox


def init():
    # Telegram event polling
    telegram.add_update_handler(update_handler)

    # UI settings
    header_text.set_align_mode('center')


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
            # @TODO: clear previous chat messages, get new from history
            print('\n')
            select_chatroom()


def select_chatroom():
    try:
        title = urwid.Text('\nTERMGRAM')
        title.set_align_mode('center')
        body = [title, urwid.Divider()]
        _, entities = telegram.get_dialogs(30)
        for entity in reversed(entities):
            label = get_display_name(entity)
            button = urwid.Button(label)
            urwid.connect_signal(button, 'click', on_selected_chatroom, entity)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
            list_conversations = urwid.ListBox(urwid.SimpleFocusListWalker(body))
            main = urwid.Padding(list_conversations, left=3, right=3)
            top = urwid.Overlay(main, urwid.SolidFill('.'),
                                align='center', width=('relative', 70),
                                valign='middle', height=('relative', 70),
                                min_width=20, min_height=9)
        global mainloop
        mainloop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
        mainloop.run()
    except KeyboardInterrupt:
        sys.exit(0)


def on_selected_chatroom(button, entity):
    global current_chat
    current_chat = entity
    global header_text
    header_text.set_text(get_display_name(entity))
    raise urwid.ExitMainLoop()


def active_chatroom():
    global message_list
    message_list = urwid.ListBox(urwid.SimpleFocusListWalker([]))
    body = urwid.LineBox(message_list)

    global mainframe
    mainframe = urwid.Frame(header=header_text, body=body, footer=input_field)
    mainframe.focus_part = 'footer'

    global mainloop
    mainloop = urwid.MainLoop(mainframe, unhandled_input=input_handler)
    mainloop.run()


def display_message(date, sender_id, message):
    date = date.strftime("%H:%M")
    sender_name = get_display_name(telegram.get_entity(sender_id))
    if not message:
        message = '{multimedia ¯\_(ツ)_/¯}'
    message = " {} | {}: {}".format(date, sender_name, message)
    message_list.body.insert(0, urwid.Text(message))
    message_list.set_focus(0)
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
    global current_chat

    if key == 'enter':
        msg = input_field.get_edit_text()
        if msg.strip():  # check for empty message
            telegram.send_message(current_chat, msg)
            display_message(datetime.datetime.now(), telegram.get_me(), msg)
            input_field.set_edit_text('')  # clear input

    elif key == 'esc':
        current_chat = None
        raise urwid.ExitMainLoop()

    elif key == 'ctrl l':
        # @TODO: clear all messages
        pass

    elif key == 'tab':
        if mainframe.focus_part == 'footer':
            mainframe.focus_part = 'body'
        else:
            mainframe.focus_part = 'footer'


def main():
    init()
    login()
    loop()


if __name__ == '__main__':
    main()
