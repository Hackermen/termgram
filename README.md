# termgram
Friendly terminal-based Telegram client.

### Dependencies
* [Python 3](https://www.python.org/)
* [Telethon](https://github.com/LonamiWebs/Telethon)
* [Urwid](https://github.com/urwid/urwid)

### Manual Install
```bash
git clone https://github.com/hackermen/termgram
cd termgram
sudo pip3 install -r requirements.txt
chmod +x termgram.py
sudo ln -s "$(pwd)/termgram.py" /usr/local/bin/termgram
```

* Generate your own API keys at https://my.telegram.org
* Add keys to `termgram/config.py`
* **Run**: `termgram`
