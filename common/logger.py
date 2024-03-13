"""Set the python logger for the project"""

import logging

__all__ = ['logger']

def set_logger() -> logging.Logger:
    """Set the logger for the project."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = set_logger()