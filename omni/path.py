"""
Module to manage paths
"""
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Union

@contextmanager
def cd(path: Union[str, Path]):
    """
    Context manager to change the current working directory
    """
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)