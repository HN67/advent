"""Solution for Day 5 of AoC."""

import collections
import dataclasses
import itertools
import logging
import sys
import typing as t

from . import core

DAY = 5

T = t.TypeVar("T")
TCo = t.TypeVar("TCo", covariant=True)

logger = logging.getLogger(__name__)

TypeT = t.TypeVar("TypeT", bound=t.Type)


@dataclasses.dataclass(frozen=True)
class Point(t.Generic[TCo]):
    """2D Point."""

    x: TCo
    y: TCo

    @classmethod
    def parse(
        cls, string: str, converter: t.Callable[[str], TCo], strip: bool = True
    ) -> "Point[TCo]":
        """Construct a Point by parsing a string.

        Parses a string of the form 'x,y',
        by default stripping any whitespace before and after each coordinate.

        Passes through each coordinate through the provided converter.

        Raises a ValueError if the string cannot be parsed,
        and propogates errors raised by the conversion converter.
        """
        if strip:
            string = string.strip()
        try:
            x_string, y_string = string.split(",")
        except ValueError as split_error:
            raise ValueError(f"Couldn't split string '{string}' on ,") from split_error

        return cls(x=converter(x_string), y=converter(y_string))


CS = t.TypeVar("CS", bound="Comparable")


class Comparable(t.Protocol):
    """Comparable/sortable protocol."""

    def __lt__(self: CS, other: CS) -> bool:
        ...


def minmax(a: CS, b: CS) -> tuple[CS, CS]:
    """Order the two parameters in ascending order."""
    left, right = sorted([a, b])
    return (left, right)


@dataclasses.dataclass(frozen=True)
class Box:
    """Euclidean 2D Box."""

    origin: Point[int]
    corner: Point[int]

    def coverage(self) -> t.Iterable[Point[int]]:
        """Return the points covered by this box."""
        min_x, max_x = minmax(self.origin.x, self.corner.x)
        min_y, max_y = minmax(self.origin.y, self.corner.y)
        # Add 1 to ends so we get inclusive ranges
        return (
            Point(x, y)
            for x in range(min_x, max_x + 1)
            for y in range(min_y, max_y + 1)
        )

    def straight_line(self) -> bool:
        """Whether the box is a straight line.

        Specifically, whether one of the coordinates is the same in origin and corner.
        """
        return self.origin.x == self.corner.x or self.origin.y == self.corner.y


def density_map(boxes: t.Iterable[Box]) -> collections.Counter[Point[int]]:
    """Overlay boxes to obtain a density map of the number of overlaps at each point."""
    return collections.Counter(
        itertools.chain.from_iterable(box.coverage() for box in boxes)
    )


def parse_line(line: str) -> Box:
    """Parse an input line into a 'Box', with origin/corner.

    Takes a line of the form 'x1,y1 -> x2,y2'.
    """
    try:
        origin_string, corner_string = line.strip().split("->")
    except ValueError as arrowException:
        raise ValueError(
            f"-> symbol does not exist as expected in string '{line}'"
        ) from arrowException
    origin = Point.parse(origin_string, converter=int)
    corner = Point.parse(corner_string, converter=int)
    return Box(origin=origin, corner=corner)


def parse_input(stream: t.TextIO) -> t.Iterable[Box]:
    """Parse puzzle input."""
    return (parse_line(line) for line in stream)


def part_one() -> None:
    """Solve Part One.

    Counts the number of points with at least two overlapping lines.
    """
    lines = parse_input(sys.stdin)
    # Only check straight lines
    density = density_map(line for line in lines if line.straight_line())
    overlaps = [point for point, number in density.items() if number > 1]
    print(f"Number of Overlaps: {len(overlaps)}")
    # TODO are we accounting for the end exclusive behaviour of ranges?
    # TODO need to ignore diagonal lines


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
