"""Solution to Day 2 of AoC."""

import enum
import logging
import typing as t

from . import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()


class RPS(enum.Enum):
    """Rock-Paper-Scissors enum."""

    ROCK = enum.auto()
    PAPER = enum.auto()
    SCISSORS = enum.auto()

    @classmethod
    def from_opponent(cls, opponent: str) -> "RPS":
        """Parse an opponent code."""
        return {"A": cls.ROCK, "B": cls.PAPER, "C": cls.SCISSORS}[opponent]

    @classmethod
    def from_player(cls, player: str) -> "RPS":
        """Parse an player code."""
        return {"X": cls.ROCK, "Y": cls.PAPER, "Z": cls.SCISSORS}[player]


# Winning plays
WINS = {(RPS.ROCK, RPS.SCISSORS), (RPS.PAPER, RPS.ROCK), (RPS.SCISSORS, RPS.PAPER)}


def result(player: RPS, opponent: RPS) -> int:
    """Compute the score from the result of a round."""
    # Player wins
    if (player, opponent) in WINS:
        return 6
    # Opponent wins
    elif (opponent, player) in WINS:
        return 0
    # Draw
    else:
        return 3


def score(player: RPS, opponent: RPS) -> int:
    """Compute the score of a round.

    Combines the score of the result and the symbol played.
    """
    plays = {RPS.ROCK: 1, RPS.PAPER: 2, RPS.SCISSORS: 3}
    return result(player, opponent) + plays[player]


def parse_game(encoding: str) -> t.Tuple[RPS, RPS]:
    """Parse a single round specification for RPS."""
    opponent, player = encoding.split()
    return (RPS.from_player(player), RPS.from_opponent(opponent))


@component.hook(2, 1)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Solve Day 2 Part 1."""
    games = [parse_game(line) for line in core.load_data(input_stream)]
    total = sum(score(player, opponent) for player, opponent in games)
    print(f"Total score: {total}", file=output_stream)
