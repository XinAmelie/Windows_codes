import logging
import time
import os
from config.settings import Settings as ST

rq = time.strftime('%Y%m%d_%H', time.localtime()) + '.log'
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class Logger(object):

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.streamHandler = logging.StreamHandler()
        self.fileHandler = logging.FileHandler(os.path.join(ST.PROJECT_ROOT, "log",rq), 'a',encoding='utf-8')
        self.formatter = logging.Formatter(format)
        self.streamHandler.setLevel(logging.DEBUG)
        self.fileHandler.setLevel(logging.DEBUG)
        self.fileHandler.setFormatter(self.formatter)
        self.streamHandler.setFormatter(self.formatter)
        # self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)

    def getLogger(self):
        return self.logger