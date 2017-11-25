import os

# Generate API keys: https://my.telegram.org/apps
TELEGRAM_ID = '' or os.environ['TELEGRAM_ID']
TELEGRAM_HASH = '' or os.environ['TELEGRAM_HASH']

CONFIG_DIR = os.path.expanduser('~') + '/.termgram/'
SESSION_FILE = CONFIG_DIR + 'auth'
IGNORE_FILE = CONFIG_DIR + 'ignore.txt'

TIMESTAMP_FORMAT = '%H:%M'

# Init
os.makedirs(CONFIG_DIR, exist_ok=True)
open(IGNORE_FILE, 'a').close()  # create empty file

APP_VERSION = 0.1
APP_LOGO = '''
         _
        | |
        | |_ ___ _ __ _ __ ___   __ _ _ __ __ _ _ __ ___
        | __/ _ \ '__| '_ ` _ \ / _` | '__/ _` | '_ ` _ \\
        | ||  __/ |  | | | | | | (_| | | | (_| | | | | | |
         \__\___|_|  |_| |_| |_|\__, |_|  \__,_|_| |_| |_|
                                 __/ |
                                |___/   v{}
        '''.format(APP_VERSION)
