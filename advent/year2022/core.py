"""Core utilities for Advent of Code 2022."""

import argparse
import collections.abc as c
import logging
import typing as t


# Adapted from HN67/nsapi
def configure_logger(
    loggerObject: logging.Logger,
    *,
    level: t.Union[int, str] = logging.WARNING,
    format_string: str = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
    force: bool = True,
) -> logging.Logger:
    """Performs standard configuration on the provided logger.

    Can be used to configure this modules logger or any user modules logger.

    Adds a default stream handler with a format string containing level, name, and message.

    Returns the logger passed.
    """
    # Add formatted handler
    # Only add the handler if forced or none exist
    if force or len(loggerObject.handlers) == 0:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(format_string))
        loggerObject.addHandler(handler)
    # Set logging level
    loggerObject.setLevel(level)
    # Chain object
    return loggerObject


def load_data(file: t.TextIO) -> c.Iterable[str]:
    """Read each line of input, stripping automatically."""
    return (line.strip() for line in file)


# Type aliases
ProblemID = t.Tuple[int, int]
# A solution is a function that is given an input and output channel,
# and we do not care about the return type of the function
Solution = t.Callable[[t.TextIO, t.TextIO], object]


class Component:
    """Intermediate holder of solutions."""

    def __init__(self) -> None:
        """Initialize a component."""
        self.solutions: t.MutableMapping[ProblemID, Solution] = {}

    def hook(
        self, day: int, part: t.Union[t.Literal[1], t.Literal[2]]
    ) -> t.Callable[[Solution], Solution]:
        """Hook a solver into the runner."""
        # Construct a closure that will add the given function to our cache
        def decorator(function: Solution) -> Solution:
            """Save the given function and return it unchanged."""
            self.solutions[day, part] = function
            return function

        # Return the constructed decorator
        return decorator


class Runner:
    """Collects and runs Advent of Code solutions."""

    def __init__(self) -> None:
        """Initalize runner."""
        self.solutions: t.MutableMapping[ProblemID, Solution] = {}

    def load_component(self, component: Component) -> None:
        """Collect solutions held in a Component."""
        self.solutions.update(component.solutions)

    def cmd(self, input_stream: t.TextIO, output_stream: t.TextIO) -> None:
        """Act as a command line script."""

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

        # Lookup the solution function, handling non existance
        try:
            solution = self.solutions[day, part]
        except KeyError:
            print(f"No solution for day {day} part {part}", file=output_stream)
            # Early return to be safe
            return
        else:
            # Run the solution, inheriting communication channels
            solution(input_stream, output_stream)
