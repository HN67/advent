"""Solution for Day 7 of AoC."""

import collections.abc as c
import logging
import statistics
import sys

from . import core

logger = logging.getLogger(__name__)

DAY = 7


def alignment_cost(positions: c.Iterable[int], target: int = 0) -> int:
    """The total cost (distance) to align each position to the target."""
    return sum(abs(pos - target) for pos in positions)


def optimal_target(positions: c.Iterable[int]) -> int:
    """The optimal alignment target."""
    return statistics.median_low(positions)


# [1, 0, 5] counter examples arithmetic mean
# [1, 3, 5] and [0, 1, 5] both have median


def part_one() -> None:
    """Solve Part One"""
    # need a list comprehension since we need to iterate over it twice
    positions = [
        int(raw) for line in core.load_data(sys.stdin) for raw in line.split(",")
    ]
    print(alignment_cost(positions, optimal_target(positions)))


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
