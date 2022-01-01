"""Solution for Day 5 of AoC."""

import logging

from . import core

logger = logging.getLogger(__name__)

DAY = 6


def part_one() -> None:
    """Solve Part One"""


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
