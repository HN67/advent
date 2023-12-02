"""Solution to Day 1 of AoC."""

import string
import logging
import typing as t

from advent import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()


def parse_numbers(lines: t.Iterable[str]) -> t.Iterable[t.Tuple[int, int]]:
    """Parse first and last digit from lines.

    If there is only a single digit,
    it is repeated. If there are no digits,
    returns (0, 0).
    """
    return (
        (0, 0) if len(digits) == 0 else (int(digits[0]), int(digits[-1]))
        for digits in (
            list(filter(lambda char: char in string.digits, line)) for line in lines
        )
    )


def find_text_numbers(text: str) -> t.Tuple[int, int]:
    """Normalize a string by replacing all spellings of digits with the actual digit."""
    digits = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }
    first = min(
        ((number, text.find(name)) for name, number in digits.items()),
        # tuples are sorted element wise; if find returned -1
        # we ensure it will be sorted after anything that was actually found
        key=lambda pair: (1 if pair[1] == -1 else 0, pair[1]),
    )
    # We still use min here because we are reversing the strings
    last = min(
        (
            (
                number,
                "".join(reversed(text)).find("".join(reversed(name))),
            )
            for name, number in digits.items()
        ),
        key=lambda pair: (1 if pair[1] == -1 else 0, pair[1]),
    )
    return (first[0], last[0])


@component.hook(1, 1, year=2023)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 1 Part 1 solution."""
    lines = core.load_data(input_stream)
    total = sum(x * 10 + y for x, y in parse_numbers(lines))
    output_stream.write(f"Total: {total}")


@component.hook(1, 2, year=2023)
def two(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 1 Part 2 solution."""
    lines = core.load_data(input_stream)
    total = sum(x * 10 + y for x, y in map(find_text_numbers, lines))
    output_stream.write(f"Total: {total}")
