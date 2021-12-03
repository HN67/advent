"""Core utilities for Advent of Code 2021."""

import argparse
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


def cmd(day: int, one: t.Callable[[], None], two: t.Callable[[], None]) -> None:
    """Act as a command line script."""

    parser = argparse.ArgumentParser(description=f"Solve AoC 2021 Day {day}.")

    parser.add_argument("part", choices=["one", "two"], help="Which part to solve")

    args = parser.parse_args()

    if args.part == "one":
        one()
    elif args.part == "two":
        two()
