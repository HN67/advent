"""Main entrypoint for Advent of Code 2022 solutions."""

import sys

from . import core
from . import day1


# Actual entrypoint
def main() -> None:
    """Main entrypoint."""
    runner = core.Runner()
    for day in (day1,):
        runner.load_component(day.component)
    runner.cmd(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
