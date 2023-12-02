"""Solution to Day 1 of AoC."""

import itertools
import logging
import typing as t

from . import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()


def parse_data(lines: t.Iterable[str]) -> t.Iterable[t.Sequence[int]]:
    """Parse elf calorie carrying from input data."""
    return (
        [int(value) for value in group]
        for key, group in itertools.groupby(lines, key=lambda line: len(line) > 0)
        if key
    )


@component.hook(1, 1, year=2022)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 1 Part 1 solution."""
    lines = core.load_data(input_stream)
    elves = parse_data(lines)
    # Real data will never be empty but for max to type correctly we should provide a default
    most: int = max(map(sum, elves), default=0)
    print(f"Most total calories: {most}", file=output_stream)


@component.hook(1, 2, year=2022)
def two(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 1 Part 2 solution."""
    lines = core.load_data(input_stream)
    elves = parse_data(lines)
    # Sort the elves carrying calories by highest first
    carries = sorted([sum(elf) for elf in elves], reverse=True)
    # Take the top 3
    top = carries[:3]
    total = sum(top)
    print(f"Top three total calories: {total}", file=output_stream)
