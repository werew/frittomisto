"""
Tests for the logging module
"""
import logging
from unittest.mock import MagicMock
from frittomisto.logging import get_logger, log_level


def test_get_logger() -> None:
    """
    Test get_logger
    """
    mock_stream = MagicMock()
    logger = get_logger("test", stream=mock_stream)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    msg = "test message"
    logger.error(msg)
    assert msg in mock_stream.write.call_args[0][0]  # type: ignore


def test_log_level() -> None:
    """
    Test log_level
    """
    logger = get_logger("test")
    logger.setLevel(logging.DEBUG)
    with log_level(logging.INFO, "test"):
        assert logger.level == logging.INFO
    with log_level(logging.WARNING, "test"):
        assert logger.level == logging.WARNING
