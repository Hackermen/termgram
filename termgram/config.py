from os import makedirs
from os.path import expanduser


TELEGRAM_ID = 
TELEGRAM_HASH = ''

CONFIG_DIR = expanduser('~') + '/.termgram/'
SESSION_FILE = CONFIG_DIR + 'auth'

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


TIMESTAMP_FORMAT = '%H:%M'


# Init
makedirs(CONFIG_DIR, exist_ok=True)
