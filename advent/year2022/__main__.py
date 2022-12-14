"""Main entrypoint for Advent of Code 2022 solutions."""

import argparse
import sys
import typing as t

# Type aliases
ProblemID = t.Tuple[int, int]
# A solution is a function that is given an input and output channel,
# and we do not care about the return type of the function
Solution = t.Callable[[t.TextIO, t.TextIO], object]


class Runner:
    """Collects and runs Advent of Code solutions."""

    def __init__(self) -> None:
        """Initalize runner."""
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
            output_stream.write(f"No solution for day {day} part {part}")
            # Early return to be safe
            return
        else:
            # Run the solution, inheriting communication channels
            solution(input_stream, output_stream)


# Actual entrypoint
def main() -> None:
    """Main entrypoint."""
    runner = Runner()
    runner.cmd(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
