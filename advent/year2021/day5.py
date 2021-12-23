"""Solution for Day 5 of AoC."""

import dataclasses
import logging
import typing as t

from . import core

DAY = 5

T = t.TypeVar("T")
TCo = t.TypeVar("TCo", covariant=True)

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Point(t.Generic[TCo]):
    """2D Point."""

    x: TCo
    y: TCo


@dataclasses.dataclass(frozen=True)
class Box(t.Generic[TCo]):
    """Euclidean 2D Box."""

    origin: Point[TCo]
    corner: Point[TCo]


def part_one() -> None:
    """Solve Part One."""


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
