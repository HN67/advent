"""Solution to Day 2 of AoC."""

import collections
import dataclasses
import functools
import logging
import math
import typing as t

from advent import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()


Selection = t.Counter[str]


@dataclasses.dataclass(frozen=True)
class Game:
    """Model a elf cube color game."""

    id: int
    reveals: t.Iterable[Selection]


def parse_game(text: str) -> Game:
    """Parse a description of a game.

    E.g. 'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'
    """

    text_id, reveals_section = text.split(":")
    game_id: int = int(text_id.split()[1])
    reveals = (
        collections.Counter(
            {
                color_components[1].strip(): int(color_components[0])
                for color_components in reveal_components
            }
        )
        for reveal_components in (
            (color_text.split() for color_text in reveal_text.split(","))
            for reveal_text in reveals_section.split(";")
        )
    )

    return Game(id=game_id, reveals=reveals)


def is_valid_game(game: Game, bag: Selection) -> bool:
    """Check if a game is valid, based on an overall selection representing an entire bag.

    A game is invalid if any reveal has more of any object than the overall bag.
    """
    return all(reveal <= bag for reveal in game.reveals)


@component.hook(2, 1, year=2023)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 2 Part 1 solution."""

    lines = core.load_data(input_stream)

    # for line in lines:
    #     game = parse_game(line)
    #     print(game.id, list(game.reveals), file=output_stream)

    DAY1_BAG = Selection({"red": 12, "green": 13, "blue": 14})

    total = sum(
        game.id
        for game in (parse_game(line) for line in lines)
        if is_valid_game(game, DAY1_BAG)
    )

    print(f"Total: {total}", file=output_stream)


def minimum_bag(reveals: t.Iterable[Selection]) -> Selection:
    """Find the smallest possible bag to make this sequence of reveals possible.

    This is exactly the union of the multisets of the reveals,
    i.e. the max seen for each colour.
    """

    # Reduce using union over the reveals iterable;
    # use an empty Counter as the initial / default value
    return functools.reduce(
        lambda accumulator, reveal: accumulator | reveal,
        reveals,
        collections.Counter(),
    )


@component.hook(2, 2, year=2023)
def two(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 2 Part 2 solution."""

    lines = core.load_data(input_stream)

    total = sum(
        math.prod(minimum_bag(game.reveals).values())
        for game in (parse_game(line) for line in lines)
    )

    print(f"Sum of powers of sets: {total}", file=output_stream)
