"""
Script for python logger setup.
"""

import logging
import sys
import os


class Logger(object):
    """
    Logger singleton class
    """

    _instance = None

    def __init__(self):
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.setup_logger()
        return cls._instance

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def setup_logger(self):
        """
        Setup for python logger.
        All messages are logged into file 'cardmaker-api.log' and stdout.
        """
        self.logger = logging.getLogger("CardmakerApi")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        level = os.getenv("LOG_LEVEL")
        if level is not None and level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif level is not None and level.lower() == "info":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        logfile = os.getenv("LOG_LOGFILE")
        if logfile is not None and logfile != "":
            file_handler = logging.FileHandler(logfile)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
