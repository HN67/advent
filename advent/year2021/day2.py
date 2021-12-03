"""Solution to Day 2 of AoC."""

import abc
import collections.abc as c
import dataclasses
import functools
import sys
import typing as t

from . import core

SU = t.TypeVar("SU", bound="Updatable")


class Updatable(t.Protocol):
    """Type that can respond to commands."""

    @abc.abstractmethod
    def update(self: SU, action: str, value: int) -> SU:
        """Create the result of a command."""


SP = t.TypeVar("SP", bound="Position")


@dataclasses.dataclass()
class Position:
    """Locate the submarine."""

    horizontal: int
    depth: int

    def __add__(self: SP, other: "Position") -> SP:
        """Element-wise sum two positions."""
        return type(self)(
            horizontal=self.horizontal + other.horizontal,
            depth=self.depth + other.depth,
        )

    def update(self: SP, action: str, value: int) -> SP:
        """Create the position resulting from a move from this position."""
        match action:
            case "forward":
                return self + Position(horizontal=value, depth=0)
            case "down":
                return self + Position(horizontal=0, depth=value)
            case "up":
                return self + Position(horizontal=0, depth=-value)
            case _:
                raise ValueError(f"Action '{action}' is not recognized.")


SS = t.TypeVar("SS", bound="State")


@dataclasses.dataclass()
class State:
    """State of a submarine, position and aim."""

    position: Position
    aim: int

    def __add__(self: SS, other: "State") -> SS:
        """Element-wise sum two states."""
        return type(self)(
            position=self.position + other.position, aim=self.aim + other.aim
        )

    def update(self: SS, action: str, value: int) -> SS:
        """Create the position resulting from a move from this position."""
        match action:
            case "forward":
                return self + State(
                    position=self.position
                    + Position(horizontal=value, depth=self.aim * value),
                    aim=0,
                )
            case "down":
                return self + State(position=Position(0, 0), aim=value)
            case "up":
                return self + State(position=Position(0, 0), aim=-value)
            case _:
                raise ValueError(f"Action '{action}' is not recognized.")


def apply_movement(initial: SU, delta: tuple[str, int]) -> SU:
    """Functionally apply a delta onto a Updatable."""
    return initial.update(delta[0], delta[1])


def chart(commands: c.Iterable[tuple[str, int]], initial: SU) -> SU:
    """Chart the resulting position based on provided commands."""
    return functools.reduce(apply_movement, commands, initial)


def parse_components(pieces: c.Sequence[str]) -> tuple[str, int]:
    """Parse the compoenents of a line into a proper pair."""
    return (pieces[0], int(pieces[1]))


def load_commands() -> t.Iterable[tuple[str, int]]:
    """Load commands from standard input."""
    return (parse_components(line.strip().split(" ")) for line in sys.stdin)


def display_result(destination: Position) -> None:
    """Format display the resulting destination."""
    print(f"Destination: {destination}")
    product = destination.horizontal * destination.depth
    print(f"Product: {product}")


def part_one() -> None:
    """Solve part one of day 2."""
    display_result(chart(load_commands(), initial=Position(0, 0)))


def part_two() -> None:
    """Solve part two of day 2."""
    display_result(chart(load_commands(), initial=State(Position(0, 0), 0)).position)


if __name__ == "__main__":
    core.cmd(2, part_one, part_two)
