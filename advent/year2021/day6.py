"""Solution for Day 5 of AoC."""

import collections.abc as c
import dataclasses
import logging
import sys
import typing as t

from . import core

logger = logging.getLogger(__name__)

DAY = 6


@dataclasses.dataclass()
class Lanternfish:
    """A fish that produces offspring periodically."""

    timer: int

    RESET = 6
    START = 8

    def tick(self) -> t.Optional["Lanternfish"]:
        """Increment time for this fish by one.

        If the fish gives birth, the new fish is returned.
        """
        self.timer -= 1
        if self.timer < 0:
            self.timer = self.RESET
            return Lanternfish(self.START)
        return None


def read_input(stream: t.TextIO) -> c.Iterable[Lanternfish]:
    """Read puzzle input."""
    return (
        Lanternfish(int(timer.strip()))
        for timer in stream.readline().strip().split(",")
    )


def advance(fishes: c.Iterable[Lanternfish]) -> c.Iterable[Lanternfish]:
    """Tick each of the provided fish, appending any new fish."""
    new = []
    for fish in fishes:
        birth = fish.tick()
        if birth:
            new.append(birth)
        yield fish
    yield from new


def simulate(fishes: c.Iterable[Lanternfish], days: int = 1) -> c.Iterable[Lanternfish]:
    """Simulates a population of Lanternfish."""
    for _ in range(days):
        fishes = advance(fishes)
    return fishes


SIMULATION_DAYS = 80


def part_one() -> None:
    """Solve Part One"""
    fishes = read_input(sys.stdin)
    end = simulate(fishes, SIMULATION_DAYS)
    print(f"Final Population: {len(list(end))}")


def part_two() -> None:
    """Solve Part Two."""


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
