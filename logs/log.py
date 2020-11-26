import os
import logging


def create_logger():
    logger = logging.getLogger("LOG")
    logger.setLevel(os.environ.get('LOG_LEVEL', logging.DEBUG))
    console_log = logging.StreamHandler()
    console_log.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s'))
    logger.addHandler(console_log)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s:'
                                  ' %(filename)s(%(funcName)s) - %(message)s')
    file_handler = logging.FileHandler("/info.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


default_logger = create_logger()
