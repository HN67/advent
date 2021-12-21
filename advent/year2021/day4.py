"""Solution for Day 4 of AoC."""

import collections.abc as c
import dataclasses
import logging
import typing as t

from . import core

TCo = t.TypeVar("TCo", covariant=True)

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Tile(t.Generic[TCo]):
    """Tile of a board."""

    value: TCo
    marked: bool


@dataclasses.dataclass()
class Board(t.Generic[TCo]):
    """Bingo board."""

    rows: c.Sequence[c.Sequence[Tile]]


def part_one() -> None:
    """Solve Part One."""


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(3, part_one, part_two)
