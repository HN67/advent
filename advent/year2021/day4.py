"""Solution for Day 4 of AoC."""

import collections.abc as c
import dataclasses
import logging
import typing as t

from . import core

T = t.TypeVar("T")
TCo = t.TypeVar("TCo", covariant=True)

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Tile(t.Generic[TCo]):
    """Tile of a board."""

    value: TCo
    marked: bool


BoardS = t.TypeVar("BoardS", bound="Board")


@dataclasses.dataclass(frozen=True)
class Board(t.Generic[T]):
    """Bingo board."""

    rows: c.Sequence[c.Sequence[Tile[T]]]

    @property
    def columns(self) -> c.Sequence[c.Sequence[Tile[T]]]:
        """Column major ordering of the board tiles."""
        return list(zip(*self.rows))

    def mark(self: BoardS, value: T) -> BoardS:
        """Create a board with any tiles containing the given value marked."""
        return type(self)(
            [
                [
                    Tile(tile.value, True) if tile.value == value else tile
                    for tile in row
                ]
                for row in self.rows
            ]
        )

    def complete(self) -> bool:
        """Whether the board has a solid row or column of marks."""
        return any(all(tile.marked for tile in row) for row in self.rows) or any(
            all(tile.marked for tile in column) for column in self.columns
        )

    def unmarked(self) -> c.Iterable[T]:
        """The values of unmarked tiles."""
        return (tile.value for row in self.rows for tile in row)


def part_one() -> None:
    """Solve Part One."""


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(3, part_one, part_two)
