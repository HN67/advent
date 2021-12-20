"""Solution for Day 3 of AoC."""

import collections.abc as c
import dataclasses
import logging
import sys
import typing as t

from . import core

logger = logging.getLogger(__name__)


@dataclasses.dataclass()
class Counter:
    """Keep track of a number of zeroes and ones."""

    zeroes: int = 0
    ones: int = 0

    def digest(self, string: str, suppress: bool = False) -> "Counter":
        """Digest a string of ones and zeroes.

        Mutates and returns this Counter.

        If suppress is True, ignores characters
        that are not '0' or '1',
        otherwise throws a ValueError.
        """
        for char in string:
            if char == "0":
                self.zeroes += 1
            elif char == "1":
                self.ones += 1
            elif not suppress:
                raise ValueError(
                    f"String passed to digest contains non-bit char '{char}'"
                )
        return self

    def frequency(self) -> tuple[bool, bool]:
        """Return the less common and most common value.

        Returns (false, true) if both are equal.
        """
        freq = (self.ones < self.zeroes, self.ones >= self.zeroes)
        logger.debug("Counter: %s | %s", self, freq)
        return freq


@dataclasses.dataclass()
class Parser:
    """Consumes diagnostic output."""

    # data[0] is data on bit 0
    # so note that this is opposite order of standard
    # representation of binary
    data: c.MutableSequence[Counter] = dataclasses.field(default_factory=list)

    def digest(self, string: str, suppress: bool = False) -> "Parser":
        """Digest a line of diagnostic output."""
        # reverse the string so we consume bits in little-endian order
        for index, char in enumerate(reversed(string)):
            try:
                self.data[index].digest(char, suppress=suppress)
            except IndexError as e:
                if index == len(self.data):
                    self.data.append(Counter().digest(char, suppress=suppress))
                else:
                    raise IndexError(
                        "Something terrible has happened and a index was skipped."
                    ) from e
        logger.debug(self.data)
        return self

    def extract(self, index: int) -> t.Iterable[bool]:
        """Calculate an extracted row,
        either min (0) or max (1).
        """
        return (d.frequency()[index] for d in self.data)

    def gamma_raw(self) -> t.Iterable[bool]:
        """Calculate the raw gamma rate."""
        return self.extract(1)

    def epsilon_raw(self) -> t.Iterable[bool]:
        """Calculate the raw epsilon rate."""
        return self.extract(0)

    @staticmethod
    def format_value(bits: t.Iterable[bool]) -> str:
        """Convert a iterable of bits into a big-endian string."""
        return "".join(reversed(["1" if bit else "0" for bit in bits]))

    def gamma(self) -> str:
        """Calculate the formatted gamma rate."""
        return Parser.format_value(self.gamma_raw())

    def epsilon(self) -> str:
        """Calculate the formatted gamma rate."""
        return Parser.format_value(self.epsilon_raw())


def parse_lines(lines: t.Iterable[str]) -> Parser:
    """Return the (gamma, epsilon) values of the given lines"""
    parser = Parser()
    for line in lines:
        parser.digest(line)
    return parser


def part_one() -> None:
    """Solve part one."""
    parser = parse_lines(core.load_data(sys.stdin))
    gamma_string = parser.gamma()
    epsilon_string = parser.epsilon()
    gamma = int(gamma_string, base=2)
    epsilon = int(epsilon_string, base=2)
    print(f"Gamma:   {gamma_string} ({gamma})")
    print(f"Epsilon: {epsilon_string} ({epsilon})")
    print(f"Power Consumption: {gamma*epsilon}")


def filter_lines(lines: t.Iterable[str], frequency_index: int) -> str:
    """Filter the list of lines by indexing progessive columns
    for either most/least common bit and only keeping matching rows.
    """
    left = list(lines)
    index = 0
    while len(left) > 1:
        parser = parse_lines((line[index] for line in left))
        bit = parser.format_value(parser.extract(frequency_index))
        left = [line for line in left if line[index] == bit]
        logger.debug("%s, %s", bit, left)
        index += 1
    return left[0]


def part_two() -> None:
    """Solve part two."""
    # Eager evaluate lines list because we need to parse it multiple times
    lines = list(core.load_data(sys.stdin))

    oxygen_string = filter_lines(lines, 1)
    co2_string = filter_lines(lines, 0)

    oxygen = int(oxygen_string, base=2)
    co2 = int(co2_string, base=2)

    print(f"Oxygen: {oxygen_string} ({oxygen})")
    print(f"CO2:    {co2_string} ({co2})")
    print(f"Life Support: {oxygen*co2}")


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(3, part_one, part_two)
