"""
Create log class for log files
"""

import logging


def get_module_logger(console=False):
    """
    Function to create logger
    :param console: Parameter to obtain or not the logger information on console
    :return: logger information
    """
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler('full.log')
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    if not console:
        return logger

    # If the user added a print to console option
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        if console.upper() == 'DEBUG':
            stream_handler.setLevel(logging.DEBUG)
        elif console.upper() == 'INFO':
            stream_handler.setLevel(logging.INFO)
        elif console.upper() == 'WARNING':
            stream_handler.setLevel(logging.WARNING)
        else:
            stream_handler.setLevel(logging.ERROR)

        return logger
