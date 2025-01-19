import logging
import pytest
from io import StringIO

from aws_api_actions.logger import (
    SUCCESS,
    OUTPUT,
    LOG_COLORS,
    ActionsFormatter,
    ActionsColoredFormatter,
    LoggerWithSuccessAndOutput,
    setup_logging,
)


def test_custom_logging_levels() -> None:
    """Test custom logging levels."""
    assert logging.getLevelName(SUCCESS) == "SUCCESS"
    assert logging.getLevelName(OUTPUT) == "OUTPUT"


def test_actions_formatter() -> None:
    """Test the ActionsFormatter class."""
    formatter = ActionsFormatter()
    record = logging.LogRecord(
        name="test",
        level=OUTPUT,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    formatted_message = formatter.format(record)
    assert formatted_message == "Test message"


def test_actions_colored_formatter() -> None:
    """Test the ActionsColoredFormatter class."""
    formatter = ActionsColoredFormatter(
        reset=True, log_colors=LOG_COLORS, style="%", secondary_log_colors=None
    )

    record = logging.LogRecord(
        name="test",
        level=OUTPUT,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    formatted_message = formatter.format(record)
    assert formatted_message == "Test message"


def test_logger_with_success_and_output() -> None:
    """Test the LoggerWithSuccessAndOutput class."""
    logger = LoggerWithSuccessAndOutput(name="test_logger")
    logger.setLevel(logging.DEBUG)

    with StringIO() as buf:
        handler = logging.StreamHandler(buf)
        logger.addHandler(handler)

        logger.success("Success message")
        logger.output("Output message")

        handler.flush()
        log_output = buf.getvalue()

    assert "Success message" in log_output
    assert "Output message" in log_output


def test_setup_logging() -> None:
    """Test the setup_logging function."""
    with StringIO() as buf:
        handler = logging.StreamHandler(buf)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

        setup_logging(color=False, verbose=True)
        root_logger.debug("Debug message")
        root_logger.info("Info message")

        handler.flush()
        log_output = buf.getvalue()

    assert "Debug message" in log_output
    assert "Info message" in log_output

    # Clean up by removing the handler
    root_logger.removeHandler(handler)
