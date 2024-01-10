"""
Test the time module
"""
import time
import pytest
from frittomisto.time import timeout


def test_timeout() -> None:
    """
    Test timeout
    """
    with timeout(1):
        pass

    with pytest.raises(TimeoutError):
        with timeout(1):
            time.sleep(2)
