"""Solution to Day 1 of AoC."""

import abc
import collections.abc as c
import typing as t
import sys

S = t.TypeVar("S")


class Comparable(t.Protocol):
    """Protocol for types that implement less than."""

    @abc.abstractmethod
    def __lt__(self: S, other: S) -> bool:
        """True if and only if self < other."""


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


def solve() -> None:
    """Entrypoint for solver.

    Handles input and output.
    """
    count = increases((line.strip() for line in sys.stdin), int)
    print(f"Increases: {count}")


# Main entrypoint
if __name__ == "__main__":
    solve()
