"""Solution to Day 1 of AoC."""

import logging
import typing as t

from . import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()


@component.hook(1, 1)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 1 Part 1 solution."""
    logger.warning("Not implemented")
