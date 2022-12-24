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

    parser.add_argument(
        "-v",
        "--verbose",
        dest="info",
        action="store_true",
        help="Enable verbose information",
    )

    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Enable debug information",
    )

    # Extract day and part
    args = parser.parse_args()

    day: int = args.day
    part: int = args.part
    logging_info: bool = args.info
    logging_debug: bool = args.debug

    # Debug flag overrides info flag
    logging_level = logging.WARNING
    if logging_info:
        logging_level = logging.INFO
    if logging_debug:
        logging_level = logging.DEBUG

    root_logger = logging.getLogger()
    core.configure_logger(root_logger, level=logging_level)

    runner = core.Runner()
    for module in MODULES:
        runner.load_component(module.component)
    runner.run(sys.stdin, sys.stdout, day=day, part=part)


if __name__ == "__main__":
    main()
