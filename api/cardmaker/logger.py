"""
Script for python logger setup.
"""

import logging
import sys


def setup_log(name, log_file, level=logging.INFO):
    """
    Setup for python logger.
    All messages are logged into file and stdout.
    """
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
