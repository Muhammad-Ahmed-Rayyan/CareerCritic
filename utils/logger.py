import logging
from config import LOG_LEVEL, LOG_FORMAT


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger configured with CareerCritic's standard format.
    Safe to call multiple times for the same name — logging.getLogger
    returns the same instance and handlers aren't duplicated.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)

    return logger