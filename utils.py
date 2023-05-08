import os

class temp_utils(object):
    USER_NAME = None
    BOT_NAME = None
    ME = None
    CURRENT = int(os.environ.get("SKIP", 0))
    CANCEL = False