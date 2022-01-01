"""Solution for Day 6 of AoC."""

import collections
import collections.abc as c
import dataclasses
import logging
import sys
import typing as t

from . import core

logger = logging.getLogger(__name__)

DAY = 6

LS = t.TypeVar("LS", bound="Lanternfish")


@dataclasses.dataclass(frozen=True)
class Lanternfish:
    """A fish that produces offspring periodically."""

    timer: int

    RESET = 6
    START = 8

    def tick(self: LS) -> tuple[LS, t.Optional["Lanternfish"]]:
        """Increment time for this fish by one.

        If the fish gives birth, the new fish is returned.
        """
        birth = None

        timer = self.timer - 1
        # Check for a new birth
        if timer < 0:
            timer = self.RESET
            birth = type(self)(timer=self.START)

        # Return updated fish and new birth if existant
        return (type(self)(timer=timer), birth)


LanternfishSwarm = collections.Counter[Lanternfish]


def compress(fishes: c.Iterable[Lanternfish]) -> LanternfishSwarm:
    """Compress fish into a swarm."""
    return collections.Counter(fishes)


def read_input(stream: t.TextIO) -> c.Iterable[Lanternfish]:
    """Read puzzle input."""
    return (
        Lanternfish(int(timer.strip()))
        for timer in stream.readline().strip().split(",")
    )


def advance(swarm: LanternfishSwarm) -> LanternfishSwarm:
    """Tick each of the provided fish, appending any new fish."""
    new: LanternfishSwarm = collections.Counter()
    for fish, count in swarm.items():
        nfish, birth = fish.tick()
        if birth:
            new[birth] += count
        new[nfish] += count
    return new


def simulate(swarm: LanternfishSwarm, days: int = 1) -> LanternfishSwarm:
    """Simulates a population of Lanternfish."""
    logger.info(swarm)
    for _ in range(days):
        swarm = advance(swarm)
        logger.info(swarm)
    return swarm


def solve(days: int) -> None:
    """Solve the puzzle to the specified simulation length."""
    fishes = read_input(sys.stdin)
    swarm = compress(fishes)
    end = simulate(swarm, days)
    print(f"Final Population: {end.total()}")


def part_one() -> None:
    """Solve Part One"""
    solve(80)


def part_two() -> None:
    """Solve Part Two."""
    solve(256)


if __name__ == "__main__":
    core.configure_logger(logger, level=logging.INFO)
    core.cmd(DAY, part_one, part_two)
