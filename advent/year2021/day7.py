"""Solution for Day 7 of AoC."""

import collections.abc as c
import functools
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


def part_one() -> None:
    """Solve Part One"""
    # need a list comprehension since we need to iterate over it twice
    positions = [
        int(raw) for line in core.load_data(sys.stdin) for raw in line.split(",")
    ]
    print(alignment_cost(positions, optimal_target(positions)))


def triangle(base: int) -> int:
    """The `base`-th triangle number.

    Equivalent to indicing the sequence [0, 1, 3, 6...
    """
    return base * (base + 1) // 2


def triangle_cost(positions: c.Iterable[int], target: int = 0) -> int:
    """The total cost (triangle of distance) to align each position to the target."""
    return sum(triangle(abs(pos - target)) for pos in positions)


def optimal_triangle_target(positions: c.Iterable[int]) -> int:
    """The optimal alignment target, based on triangle distance."""
    # Ensure we can iterate multiple times
    positions = tuple(positions)
    return min(
        (
            target
            for target in range(
                min(positions),
                max(positions) + 1,
            )
        ),
        key=functools.partial(triangle_cost, positions),
    )


def part_two() -> None:
    """Solve Part Two."""
    positions = [
        int(raw) for line in core.load_data(sys.stdin) for raw in line.split(",")
    ]
    print(triangle_cost(positions, optimal_triangle_target(positions)))


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
