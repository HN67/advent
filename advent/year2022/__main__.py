"""Main entrypoint for Advent of Code 2022 solutions."""

import logging
import sys

from . import core
from . import day1

logger = logging.getLogger(__name__)


# Actual entrypoint
def main() -> None:
    """Main entrypoint."""
    root_logger = logging.getLogger()
    core.configure_logger(root_logger)

    runner = core.Runner()
    for day in (day1,):
        runner.load_component(day.component)
    runner.cmd(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
