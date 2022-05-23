"""This module contains helper functions for logging"""
import logging

LEVEL_MAP = {
    "debug": logging.debug,
    "info": logging.info,
    "warning": logging.warning,
    "error": logging.error,
    "critical": logging.critical,
}


def append_logging_prefix(log_msg: str, logging_prefix: str) -> str:
    """Appends the logging prefix onto a log message in square brackets

    Parameters
    ----------
    log_msg : str
        Message for logging
    logging_prefix : str
        Logging prefix (usually the name of the module/submodule)

    Returns
    -------
    str
        Message with bracketed prefix
    """
    return f"[{logging_prefix}] " + log_msg


def log_with_prefix(log_msg: str, logging_prefix: str, level: str = "info"):
    """Log a message with a square bracketed prefix

    Parameters
    ----------
    log_msg : str
        Message for logging
    logging_prefix : str
        Logging prefix (usually the name of the module/submodule)
    level : str, optional
        What level to log at (string version of 'logging.x' eg. "info" or "debug"), by default "info"
    """
    LEVEL_MAP[level](append_logging_prefix(log_msg, logging_prefix))
