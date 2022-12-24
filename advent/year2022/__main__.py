"""Main entrypoint for Advent of Code 2022 solutions."""

import argparse
import logging
import sys

from . import core
from . import day1
from . import day2

MODULES = (day1, day2)

logger = logging.getLogger(__name__)


# Actual entrypoint
def main() -> None:
    """Main entrypoint."""

    # Set up cmdline argument parser
    parser = argparse.ArgumentParser(description="Solve AoC 2022 problems.")

    # Not really practical to restrict the choice of day
    parser.add_argument("day", help="Which day to solve", type=int)
    # Doing numbers for part makes type conversion easier
    parser.add_argument(
        "part",
        choices=[1, 2],
        help="Which part to solve",
        const=1,
        default=1,
        nargs="?",
        type=int,
    )

    # Extract day and part
    args = parser.parse_args()

    day: int = args.day
    part: int = args.part

    root_logger = logging.getLogger()
    core.configure_logger(root_logger, level=logging.INFO)

    runner = core.Runner()
    for module in MODULES:
        runner.load_component(module.component)
    runner.run(sys.stdin, sys.stdout, day=day, part=part)


if __name__ == "__main__":
    main()
