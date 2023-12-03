"""Solution to Day 3 of AoC."""

import dataclasses
import logging
import re
import typing as t

from advent import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()

Coord = t.Tuple[int, int]


@dataclasses.dataclass(frozen=True)
class EngineSchematic:
    """An engine schematic"""

    # Mapping of left/start locations to numbers
    # and locations to symbols
    numbers: t.Mapping[Coord, t.Tuple[int, Coord]]
    symbols: t.Mapping[Coord, str]

    @classmethod
    def from_text(cls, lines: t.Iterable[str]) -> "EngineSchematic":
        """Parse an engine schematic from a list of lines.

        Interprets the text with 0-based indices.
        """

        parsed_lines = (
            (
                {
                    # match.end gives a exlusive bound;
                    # for our purposes we want the inclusive coordinate
                    (row, match.start()): (int(match.group()), (row, match.end() - 1))
                    for match in re.finditer(r"\d+", line)
                },
                {
                    (row, match.start()): match.group()
                    for match in re.finditer(r"[^.0-9]", line)
                },
            )
            for row, line in enumerate(lines)
        )

        numbers: t.Mapping[Coord, t.Tuple[int, Coord]] = {}
        symbols: t.Mapping[Coord, str] = {}

        for line_numbers, line_symbols in parsed_lines:
            numbers |= line_numbers
            symbols |= line_symbols

        return cls(numbers=numbers, symbols=symbols)


def part_numbers(schematic: EngineSchematic) -> t.Iterable[int]:
    """Retrive all the part numbers from a schematic.

    A part number is a number adjacent to a symbol,
    even diagonally, at any point along the number.
    """

    return (
        number
        for start, (number, end) in schematic.numbers.items()
        if any(
            (row, col) in schematic.symbols
            for row in (start[0] - 1, start[0], start[0] + 1)
            # range is end-exclusive so add 1 to the + 1
            for col in range(start[1] - 1, end[1] + 1 + 1)
        )
    )


def adjacent_numbers(spot: Coord, schematic: EngineSchematic) -> t.Iterable[int]:
    """Find all numbers adjacent to a coordinate."""
    return (
        number
        for start, (number, end) in schematic.numbers.items()
        if spot
        in (
            (row, col)
            for row in (start[0] - 1, start[0], start[0] + 1)
            # range is end-exclusive so add 1 to the + 1
            for col in range(start[1] - 1, end[1] + 1 + 1)
        )
    )


def gears(schematic: EngineSchematic) -> t.Iterable[int]:
    """Find all gear products of the schematic."""
    return (
        numbers[0] * numbers[1]
        for numbers in (
            list(adjacent_numbers(coord, schematic))
            for coord, symbol in schematic.symbols.items()
            if symbol == "*"
        )
        if len(numbers) == 2
    )


@component.hook(3, 1, year=2023)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 3 Part 1 solution."""

    lines = core.load_data(input_stream)

    schematic = EngineSchematic.from_text(lines)

    total = sum(part_numbers(schematic))

    print(f"Total: {total}", file=output_stream)


@component.hook(3, 2, year=2023)
def two(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 3 Part 2 solution."""

    lines = core.load_data(input_stream)

    schematic = EngineSchematic.from_text(lines)

    total = sum(gears(schematic))

    print(f"Sum of gear ratios: {total}", file=output_stream)
