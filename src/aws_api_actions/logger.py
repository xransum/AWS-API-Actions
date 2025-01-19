import logging
from typing import Any, cast

from colorlog import ColoredFormatter


# Custom logging levels
SUCCESS = 25  # set between standard INFO: 20 and WARNING:30 level
OUTPUT = logging.DEBUG
LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "blue",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white",
    "SUCCESS": "green",
}


def _get_format(colorlog: bool) -> str:
    """Helper to return the log format based on color setting."""
    if colorlog:
        return "%(log_color)s%(levelname)s%(reset)s: %(log_color)s%(message)s%(reset)s"

    return "%(levelname)s: %(message)s"


class ActionsFormatter(logging.Formatter):
    """Formatter for non-colored logs."""

    def __init__(self) -> None:
        super().__init__(fmt=_get_format(colorlog=False))
        self._simple_fmt = logging.Formatter("%(message)s")

    def format(self, record: Any) -> str:
        """Format the log record, applying simpler format for OUTPUT level."""
        if record.levelname == "OUTPUT":
            return self._simple_fmt.format(record)

        return super().format(record)


class ActionsColoredFormatter(ColoredFormatter):
    """Formatter for colored logs."""

    def __init__(
        self,
        datefmt: Any = None,
        style: Any = None,
        log_colors: Any = None,
        reset: bool = True,
        secondary_log_colors: Any = None,
    ) -> None:
        """Initialize the formatter with color settings.

        Args:
            datefmt (Any, optional): Format string for the date. Defaults to
                None.
            style (Any, optional): Format string style. Defaults to None.
            log_colors (Any, optional): Dictionary of log colors. Defaults to
                None.
            reset (bool, optional): Whether to reset the color. Defaults to True.
            secondary_log_colors (Any, optional): Dictionary of secondary log
                colors. Defaults to None.
        """
        super().__init__(
            fmt=_get_format(colorlog=True),
            datefmt=datefmt,
            style=style,
            log_colors=log_colors,
            reset=reset,
            secondary_log_colors=secondary_log_colors,
        )
        self._simple_fmt = logging.Formatter("%(message)s")

    def format(self, record: Any) -> str:
        """Format the log record, applying simpler format for OUTPUT level."""
        if record.levelname == "OUTPUT":
            return self._simple_fmt.format(record)

        return super().format(record)


class LoggerWithSuccessAndOutput(logging.Logger):
    """Logger class with custom SUCCESS and OUTPUT log levels."""

    def __init__(self, name: str, level: int = logging.NOTSET):
        """Initialize the logger with custom log levels."""
        super().__init__(name, level)
        logging.addLevelName(SUCCESS, "SUCCESS")
        logging.addLevelName(OUTPUT, "OUTPUT")

    def success(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a message with SUCCESS level."""
        if self.isEnabledFor(SUCCESS):  # pragma: no cover
            self._log(SUCCESS, msg, args, **kwargs)

    def output(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a message with OUTPUT level."""
        if self.isEnabledFor(OUTPUT):  # pragma: no cover
            self._log(OUTPUT, msg, args, **kwargs)


# Set the custom logger class
logging.setLoggerClass(LoggerWithSuccessAndOutput)
logger = cast(LoggerWithSuccessAndOutput, logging.getLogger("aws-api-actions"))


def _get_formatter(color: bool) -> logging.Formatter:
    """Return appropriate formatter based on color setting."""
    if color:
        return ActionsColoredFormatter(
            reset=True,
            log_colors=LOG_COLORS,
            style="%",
            secondary_log_colors=None,
        )

    return ActionsFormatter()


def setup_logging(color: bool, verbose: bool = False) -> None:
    """Setup logging configuration for the application.

    Args:
        color (bool): If true, logs will be colored using colorlog.
        verbose (bool): If true, sets the root logger to OUTPUT level.
    """

    # Get the root logger
    root_logger = logging.getLogger()

    # Set log level based on verbosity
    if verbose:
        root_logger.setLevel(OUTPUT)
    else:
        root_logger.setLevel(logging.INFO)

    # Add a new handler with the appropriate formatter
    handler = logging.StreamHandler()
    handler.setFormatter(_get_formatter(color))
    root_logger.addHandler(handler)

    # Silence noisy external loggers
    logging.getLogger("sh").setLevel(logging.WARNING)
