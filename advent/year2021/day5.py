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


def span(start: int, end: int) -> range:
    """Create an appropriate range object.

    Creates a range over the inclusive interval [start, end],
    (i.e shifting end param to accomodate `range` exclusive behaviour)
    and automatically uses a negative step if start > end.
    """
    if start > end:
        step = -1
    else:
        step = 1
    return range(start, end + step, step)


@dataclasses.dataclass(frozen=True)
class Line:
    """Euclidean 2D Box."""

    origin: Point[int]
    end: Point[int]

    def coverage(self) -> t.Iterable[Point[int]]:
        """Return the points covered by this line.

        Returns an undefined set when the line is not straight or 45 degrees.
        """
        # Span the two axes
        x_span = span(self.origin.x, self.end.x)
        y_span = span(self.origin.y, self.end.y)
        # A 45 degree line will zip together perfectly
        # but we need to special case straight ones
        x_iter: t.Iterable[int] = x_span
        y_iter: t.Iterable[int] = y_span
        if self.vertical():
            x_iter = itertools.repeat(self.origin.x, len(y_span))
        if self.horizontal():
            y_iter = itertools.repeat(self.origin.y, len(x_span))
        # Return the iter of points
        return (Point(x, y) for x, y in zip(x_iter, y_iter))

    def vertical(self) -> bool:
        """Whether the line is a straight vertical line."""
        return self.origin.x == self.end.x

    def horizontal(self) -> bool:
        """Whether the line is a straight horizontal line."""
        return self.origin.y == self.end.y

    def straight_line(self) -> bool:
        """Whether the line is a straight line.

        Specifically, whether one of the coordinates is the same in origin and end.
        """
        return self.vertical() or self.horizontal()


def density_map(lines: t.Iterable[Line]) -> collections.Counter[Point[int]]:
    """Overlay lines to obtain a density map of the number of overlaps at each point."""
    return collections.Counter(
        itertools.chain.from_iterable(line.coverage() for line in lines)
    )


def parse_line(line: str) -> Line:
    """Parse an input line into a 'Line', with origin/end.

    Takes a line of the form 'x1,y1 -> x2,y2'.
    """
    try:
        origin_string, end_string = line.strip().split("->")
    except ValueError as arrowException:
        raise ValueError(
            f"-> symbol does not exist as expected in string '{line}'"
        ) from arrowException
    origin = Point.parse(origin_string, converter=int)
    end = Point.parse(end_string, converter=int)
    return Line(origin=origin, end=end)


def parse_input(stream: t.TextIO) -> t.Iterable[Line]:
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


def part_two() -> None:
    """Solve Part Two."""
    lines = parse_input(sys.stdin)
    # Only check straight lines
    density = density_map(lines)
    overlaps = [point for point, number in density.items() if number > 1]
    print(f"Number of Overlaps: {len(overlaps)}")


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
