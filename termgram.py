#!/usr/bin/env python3
import sys

import urwid
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty


API_ID = 117120
API_HASH = '4f3d31306935d48f1c9cc42b75838521'
client = TelegramClient('termgram', API_ID, API_HASH)
selected_chat = None


def login():
    client.connect()
    if not client.is_user_authorized():
        phone = input("Phone number: ")
        client.sign_in(phone=phone)
        code = input("Activation code: ")
        client.sign_in(code=code)
        if not client.is_user_authorized():
            print("Invalid code. Try again.")
            sys.exit(1)


def select_chatroom():
    results = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=10
    ))

    chatrooms = {}
    id_count = 0
    for group in results.chats:
        chatrooms[id_count] = ('group', group.id, group.title)
        id_count += 1
        print("{}: {} (Group)".format(id_count, group.title))
    for user in results.users:
        full_name = user.first_name
        if user.last_name:
            full_name += " " + user.last_name
        chatrooms[id_count] = ('user', user.id, full_name)
        id_count += 1
        print("{}: {} (User)".format(id_count, full_name))

    answer = int(input("\nSelect chat ID: "))
    global selected_chat
    selected_chat = chatrooms[answer]


def main():
    login()
    select_chatroom()


if __name__ == '__main__':
    main()
