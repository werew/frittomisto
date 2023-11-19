"""
Utilities for logging
"""
import logging
from typing import Optional, Generator, Union
from contextlib import contextmanager
from functools import lru_cache

@lru_cache(maxsize=None) # Cache the result to avoid registering the same handler multiple times
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Returns a logger with the given name.
    Set the level of the logger with logger.setLevel(logging.DEBUG)
    """
    if name is None:
        logger = logging.getLogger()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    else:
        logger = logging.getLogger(name)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger

@contextmanager
def log_level(level: Union[int, str], name: Optional[str] = None) -> Generator[None, None, None]:
    """
    Context manager to set the log level for the given logger
    """
    logger = logging.getLogger(name)
    original_level = logger.level
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(original_level)
