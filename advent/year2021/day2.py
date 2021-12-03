"""Solution to Day 2 of AoC."""

import collections.abc as c
import dataclasses
import functools
import sys
import typing as t

from . import core

S = t.TypeVar("S", bound="Position")


@dataclasses.dataclass()
class Position:
    """Locate the submarine."""

    horizontal: int
    depth: int

    def __add__(self: S, other: "Position") -> S:
        """Element-wise sum two positions."""
        return type(self)(
            horizontal=self.horizontal + other.horizontal,
            depth=self.depth + other.depth,
        )

    def move(self, action: str, distance: int) -> "Position":
        """Create the position resulting from a move from this position."""
        match action:
            case "forward":
                return self + Position(horizontal=distance, depth=0)
            case "down":
                return self + Position(horizontal=0, depth=distance)
            case "up":
                return self + Position(horizontal=0, depth=-distance)
            case _:
                raise ValueError(f"Action '{action}' is not recognized.")


def apply_movement(initial: Position, delta: tuple[str, int]) -> Position:
    """Functionally apply a delta onto a Position."""
    return initial.move(delta[0], delta[1])


def chart(
    commands: c.Iterable[tuple[str, int]], initial: t.Optional[Position] = None
) -> Position:
    """Chart the resulting position based on provided commands."""
    if initial is None:
        initial = Position(0, 0)
    return functools.reduce(apply_movement, commands, initial)


def parse_components(pieces: c.Sequence[str]) -> tuple[str, int]:
    """Parse the compoenents of a line into a proper pair."""
    return (pieces[0], int(pieces[1]))


def part_one() -> None:
    """Solve part one of day 2."""
    commands: t.Iterable[tuple[str, int]] = (
        parse_components(line.strip().split(" ")) for line in sys.stdin
    )
    destination = chart(commands)
    print(f"Destination: {destination}")
    product = destination.horizontal * destination.depth
    print(f"Product: {product}")


def part_two() -> None:
    """Solve part two of day 2."""
    return apply_movement(3, "2")


if __name__ == "__main__":
    core.cmd(2, part_one, part_two)
