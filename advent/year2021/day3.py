"""Solution for Day 3 of AoC."""

import collections.abc as c
import dataclasses
import sys
import typing as t

from . import core


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
        return (self.ones < self.zeroes, self.ones >= self.zeroes)


@dataclasses.dataclass()
class Parser:
    """Consumes diagnostic output."""

    # data[0] is data on bit 0
    # so note that this is opposite order of standard
    # representation of binary
    data: c.MutableSequence[Counter] = dataclasses.field(default_factory=list)

    def digest(self, string: str, suppress: bool = False) -> "Parser":
        """Digest a line of diagnostic output."""
        for index, char in enumerate(string):
            try:
                self.data[index].digest(char, suppress=suppress)
            except IndexError as e:
                if index == len(self.data):
                    self.data.append(Counter().digest(char, suppress=suppress))
                else:
                    raise IndexError(
                        "Something terrible has happened and a index was skipped."
                    ) from e
        return self

    def gamma(self) -> t.Iterable[bool]:
        """Calculate the gamma rate."""
        return (d.frequency()[1] for d in self.data)

    def epsilon(self) -> t.Iterable[bool]:
        """Calculate the epsilon rate."""
        return (d.frequency()[0] for d in self.data)

    @staticmethod
    def format_value(bits: t.Iterable[bool]) -> str:
        """Convert a iterable of bits into a big-endian string."""
        return "".join(reversed(["1" if bit else "0" for bit in bits]))


def part_one() -> None:
    """Solve part one."""
    parser = Parser()
    for line in core.load_data(sys.stdin):
        parser.digest(line)
    gamma_string = Parser.format_value(parser.gamma())
    epsilon_string = Parser.format_value(parser.epsilon())
    gamma = int(gamma_string, base=2)
    epsilon = int(epsilon_string, base=2)
    print(f"Gamma:   {gamma_string} ({gamma})")
    print(f"Epsilon: {epsilon_string} ({epsilon})")
    print(f"Power Consumption: {gamma*epsilon}")


def part_two() -> None:
    """Solve part two."""


if __name__ == "__main__":
    core.cmd(3, part_one, part_two)
