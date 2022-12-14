"""Core utilities for Advent of Code 2022."""

import collections.abc as c
import logging
import typing as t


# Adapted from HN67/nsapi
def configure_logger(
    loggerObject: logging.Logger,
    *,
    level: t.Union[int, str] = logging.WARNING,
    format_string: str = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
    force: bool = True,
) -> logging.Logger:
    """Performs standard configuration on the provided logger.

    Can be used to configure this modules logger or any user modules logger.

    Adds a default stream handler with a format string containing level, name, and message.

    Returns the logger passed.
    """
    # Add formatted handler
    # Only add the handler if forced or none exist
    if force or len(loggerObject.handlers) == 0:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(format_string))
        loggerObject.addHandler(handler)
    # Set logging level
    loggerObject.setLevel(level)
    # Chain object
    return loggerObject


def load_data(file: t.TextIO) -> c.Iterable[str]:
    """Read each line of input, stripping automatically."""
    return (line.strip() for line in file)
