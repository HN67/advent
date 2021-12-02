"""Solution to Day 1 of AoC."""

import abc
import argparse
import collections
import collections.abc as c
import functools
import operator
import typing as t
import sys

S = t.TypeVar("S")


class Comparable(t.Protocol):
    """Protocol for types that implement less than."""

    @abc.abstractmethod
    def __lt__(self: S, other: S) -> bool:
        """True if and only if self < other."""


class Addable(t.Protocol):
    """Protocol for types that implement addition."""

    @abc.abstractmethod
    def __add__(self: S, other: S) -> S:
        """Return self + other."""


CT = t.TypeVar("CT", bound=Comparable)
T = t.TypeVar("T")


def increases(measures: c.Iterable[T], key: t.Callable[[T], CT]) -> int:
    """Calculate the number of increasing measurements."""
    last: t.Optional[CT] = None
    count = 0
    for measure in measures:
        keyed = key(measure)
        if last is not None and last < keyed:
            count += 1
        last = keyed
    return count


AT = t.TypeVar("AT", bound=Addable)


def compress_sliding_windows(
    values: c.Iterable[AT], window_size: int = 1
) -> c.Iterable[AT]:
    """Compute the iterable of sums of sliding windows.

    Acts as an identity function (under ==) when window_size = 1.

    Returns an empty iterable if there are not enough values to fill a window.
    """
    window: collections.deque[AT] = collections.deque(maxlen=window_size)
    for value in values:
        window.append(value)
        # we don't want to start yielding until full window
        if len(window) == window_size:
            # sum is too concrete to use effectively
            # omitting a initial makes it use 0
            yield functools.reduce(operator.add, window)


def part_one() -> None:
    """Entrypoint for solver.

    Handles input and output.
    """
    count = increases((line.strip() for line in sys.stdin), int)
    print(f"Increases: {count}")


def part_two() -> None:
    """Entrypoint for part two.

    Handles input and output.
    """
    converted: t.Iterable[int] = map(int, (line.strip() for line in sys.stdin))
    count = increases(compress_sliding_windows(converted, 3), int)
    print(f"Sliding Increases: {count}")


def cmd() -> None:
    """Act as a command line script."""

    parser = argparse.ArgumentParser(description="Solve AoC 2021 Day 1.")

    parser.add_argument("part", choices=["one", "two"], help="Which part to solve")

    args = parser.parse_args()

    if args.part == "one":
        part_one()
    elif args.part == "two":
        part_two()


# Main entrypoint
if __name__ == "__main__":
    cmd()
