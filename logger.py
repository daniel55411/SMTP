import logging
import sys


class log_level:
    DEBUG = logging.debug
    ERROR = logging.error
    INFO = logging.info
    WARNING = logging.warning


class Logger:
    def __init__(self):
        self.disabled = False
        logging.basicConfig(level=logging.DEBUG, filename='app.log',
                            format=u'%(levelname)s\t[%(asctime)s]  %(message)s')

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def log(self, level, message):
        def logger(f):
            def g(*args, **kwargs):
                if not self.disabled:
                    level(message)
                return f(*args, **kwargs)
            return g
        return logger

    def register(self, level, message):
        if not self.disabled:
            level(message)
