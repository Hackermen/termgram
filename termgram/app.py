import datetime
import sys

import urwid
import telethon
from telethon.tl import types
from telethon.utils import get_display_name

from termgram import config


# Telegram (Telethon)
client = None  # type: telethon.TelegramClient
current_chat = None  # type: telethon.types.User|Channel

# UI (Urwid)
mainloop = None  # type: urwid.MainLoop
mainframe = None  # type: urwid.Frame
message_list = None  # type: urwid.ListBox
header_text = None  # type: urwid.Text
input_field = None  # type: urwid.Edit


def run():
    init()
    login()
    loop()
    exit_program()


def init():
    # Telegram
    if not any([config.TELEGRAM_ID, config.TELEGRAM_HASH]):
        print("Missing Telegram API keys at config.py")
        sys.exit(1)
    global client
    client = telethon.TelegramClient(config.SESSION_FILE, config.TELEGRAM_ID, config.TELEGRAM_HASH, update_workers=1)
    client.add_update_handler(event_polling)

    # UI
    global header_text
    header_text = urwid.Text('termgram')
    header_text.set_align_mode('center')
    global input_field
    input_field = urwid.Edit('> ')


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
            exit_program()


def loop():
    live_chatroom()


def event_polling(update):
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
        my_message = input_field.get_edit_text()
        if my_message.strip() and current_chat:
            client.send_message(current_chat, my_message)
            display_message(datetime.datetime.now(), client.get_me(), my_message)
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


def live_chatroom():
    global message_list
    message_list = urwid.ListBox(urwid.SimpleFocusListWalker([]))
    body = urwid.LineBox(message_list)

    global mainframe
    mainframe = urwid.Frame(header=header_text, body=body, footer=input_field)
    mainframe.focus_part = 'footer'

    global columns
    columns = urwid.Columns([build_contact_list(), mainframe])

    global mainloop
    mainloop = urwid.MainLoop(columns, unhandled_input=input_handler)

    try:
        mainloop.run()
    except KeyboardInterrupt:
        exit_program()


def build_contact_list():
    body = []
    _, entities = client.get_dialogs(50)
    for entity in reversed(entities):
        label = get_display_name(entity)
        button = urwid.Button(label)
        urwid.connect_signal(button, 'click', on_selected_chatroom, entity)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    list_conversations = urwid.ListBox(urwid.SimpleFocusListWalker(body))
    main = urwid.Padding(list_conversations, left=7, right=7)
    return main


def on_selected_chatroom(event, entity):
    global current_chat
    current_chat = entity
    global header_text
    header_text.set_text(get_display_name(entity))
    columns.set_focus_column(1)
    # retrieve recent chat (history)
    total, messages, senders = client.get_message_history(entity)
    for message in messages:
        display_message(message.date, message.from_id, message.message)


def display_message(date, sender_id, message):
    date = date.strftime(config.TIMESTAMP_FORMAT)
    sender_name = get_display_name(sender_id)
    if not message:
        message = '{multimedia ¯\_(ツ)_/¯}'
    message = " {} | {}: {}".format(date, sender_name, message)
    message_list.body.insert(0, urwid.Text(message))
    message_list.set_focus(0)
    mainloop.draw_screen()


def exit_program():
    client.disconnect()
    sys.exit(0)
