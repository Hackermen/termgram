import re

from termgram import config


class IgnoreFeature:
    """Don't display a message containing lines from ~/.termgram/ignore.txt

    Regex is considered if line starts and ends with a slash. (case insensitive)
    """

    def __init__(self):
        self.pattern_list = []
        self.refresh()

    def refresh(self):
        self.pattern_list = []
        with open(config.IGNORE_FILE, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line:
                    self.pattern_list.append(line)

    def check(self, message):
        for pattern in self.pattern_list:
            # Use Regex
            if pattern[0] == '/' and pattern[-1] == '/':
                if re.match(pattern[1:-1], message.strip(), re.IGNORECASE):
                    return True
            # Simple string match
            else:
                if pattern.lower() in message.strip().lower():
                    return True
