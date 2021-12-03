"""Core utilities for Advent of Code 2021."""

import argparse
import typing as t


def cmd(day: int, one: t.Callable[[], None], two: t.Callable[[], None]) -> None:
    """Act as a command line script."""

    parser = argparse.ArgumentParser(description=f"Solve AoC 2021 Day {day}.")

    parser.add_argument("part", choices=["one", "two"], help="Which part to solve")

    args = parser.parse_args()

    if args.part == "one":
        one()
    elif args.part == "two":
        two()
