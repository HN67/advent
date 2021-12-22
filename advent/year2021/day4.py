"""Solution for Day 4 of AoC."""

import collections.abc as c
import dataclasses
import itertools
import logging
import sys
import typing as t

from . import core

T = t.TypeVar("T")
TCo = t.TypeVar("TCo", covariant=True)

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Tile(t.Generic[TCo]):
    """Tile of a board."""

    value: TCo
    marked: bool = False


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
        return (tile.value for row in self.rows for tile in row if not tile.marked)


def read_input() -> tuple[c.Iterable[int], c.Iterable[Board[int]]]:
    """Read the puzzle input."""

    # Get the called numbers
    calls = [int(number) for number in input().split(",")]

    # Advance stdin
    input()

    boards = [
        Board(
            # Whitespace split() consumes multiple spaces
            [[Tile(int(number)) for number in row.strip().split()] for row in group]
        )
        for key, group in itertools.groupby(sys.stdin, key=lambda line: line == "\n")
        if not key
    ]

    return calls, boards


def winner(
    calls: c.Iterable[T], boards: c.Iterable[Board[T]]
) -> t.Optional[tuple[T, Board[T]]]:
    """Find the first winning board.

    Iterates calls until a winning board is found,
    returning it.

    Returns the first board in the iterable if multiple win simultaneously.

    Returns None if no boards win after calls is exhausted.
    """
    for call in calls:
        # Mark the call
        boards = [board.mark(call) for board in boards]
        # Check for a winner
        for board in boards:
            if board.complete():
                return call, board
    return None


def valuate(call: int, board: Board[int]) -> int:
    """The value of a completed board with the winning call."""
    return sum(board.unmarked()) * call


def part_one() -> None:
    """Solve Part One."""
    calls, boards = read_input()
    winning = winner(calls, boards)
    if winning is None:
        print("No winner.")
    else:
        call, board = winning
        print(f"Call: {call}")
        print(f"Board: {board}")
        print(f"Score: {valuate(call, board)}")


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(3, part_one, part_two)
