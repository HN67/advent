"""Core utilities for Advent of Code."""

import collections.abc as c
import dataclasses
import logging
import typing as t


# Adapted from HN67/nsapi
def configure_logger(
    loggerObject: logging.Logger,
    *,
    level: t.Union[int, str] = logging.WARNING,
    format_string: t.Optional[str] = None,
    force: bool = True,
) -> logging.Logger:
    """Performs standard configuration on the provided logger.

    Can be used to configure this modules logger or any user modules logger.

    Adds a default stream handler with a format string containing level, name, and message.

    Returns the logger passed.
    """
    # Set format_string to default if not provided
    if format_string is None:
        format_string = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"

    # Add formatted handler
    # Only add the handler if forced or none exist
    if force or len(loggerObject.handlers) == 0:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(format_string))
        loggerObject.addHandler(handler)

    # Set logging level
    loggerObject.setLevel(level)

    # Return object so this function can be chained
    return loggerObject


def load_data(file: t.TextIO) -> c.Iterable[str]:
    """Read each line of input, stripping automatically."""
    return (line.strip() for line in file)


# Type aliases
@dataclasses.dataclass(frozen=True)
class ProblemID:
    """Identify a problem."""

    year: int
    day: int
    part: int


# A solution is a function that is given an input and output channel,
# and we do not care about the return type of the function
Solution = t.Callable[[t.TextIO, t.TextIO], object]


class Component:
    """Intermediate holder of solutions."""

    def __init__(self) -> None:
        """Initialize a component."""
        self.solutions: t.MutableMapping[ProblemID, Solution] = {}

    def hook(
        self, day: int, part: int, *, year: int
    ) -> t.Callable[[Solution], Solution]:
        """Hook a solver into the runner."""

        # Construct a closure that will add the given function to our cache
        def decorator(function: Solution) -> Solution:
            """Save the given function and return it unchanged."""
            self.solutions[ProblemID(year=year, day=day, part=part)] = function
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

    def run(
        self, input_stream: t.TextIO, output_stream: t.TextIO, *, problem: ProblemID
    ) -> None:
        """Run the requested solution using the given communication channels."""

        # Lookup the solution function, handling non existance
        try:
            solution = self.solutions[problem]
        except KeyError:
            print(
                f"No solution for {problem.year} day {problem.day} part {problem.part}",
                file=output_stream,
            )
            # Early return to be safe
            return
        else:
            # Run the solution, inheriting communication channels
            solution(input_stream, output_stream)
