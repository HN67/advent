"""Solution to Day 4 of AoC."""

import dataclasses
import logging
import typing as t

from advent import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()


@dataclasses.dataclass(frozen=True)
class Scratchcard:
    """Data of a scratchcard."""

    id: int
    winners: t.Container[int]
    numbers: t.Iterable[int]


def parse_scratchcard(text: str) -> Scratchcard:
    """Parse the textual representation of a scratchcard.

    For example, 'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    where the id=1, winners={41, 48, 83, 86, 17},
    and numbers={83, 86, 6, 31, 17, 9, 48, 53}.
    """
    name, info = text.split(":", maxsplit=1)
    card_id = int(name.split()[1].strip())
    winners_text, numbers_text = info.split("|", maxsplit=1)
    winners = {int(value) for value in winners_text.split()}
    numbers = (int(value) for value in numbers_text.split())

    return Scratchcard(id=card_id, winners=winners, numbers=numbers)


def card_wins(card: Scratchcard) -> int:
    """Determine the amount of wins on a scratchcard."""
    return sum(1 for number in card.numbers if number in card.winners)


def card_worth(card: Scratchcard) -> int:
    """Determine the value of a scratchcard.

    The first number that is a winner makes the card worth one point,
    and every subsequent number doubles the value.
    """
    # Count the number of matches
    matches = card_wins(card)
    if matches == 0:
        return 0
    # Doubling each time can be computed with 2^(# - 1)
    return 2 ** (matches - 1)


@component.hook(4, 1, year=2023)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 4 Part 1 solution."""

    lines = core.load_data(input_stream)

    total = sum(card_worth(parse_scratchcard(line)) for line in lines)

    print(f"Total worth: {total}", file=output_stream)


def process_deck(deck: t.Iterable[Scratchcard]) -> int:
    """Process a deck of scratchcards using win copies rules.

    Counts the total number of cards obtained.
    """

    hand: t.MutableMapping[int, t.Tuple[Scratchcard, int]] = {
        card.id: (card, 1) for card in deck
    }

    # Since cards always yield copies of subsequent cards,
    # we can single iterate through in ascending order
    for card_id in sorted(hand.keys()):
        # Find how many wins one of this card has
        matches = card_wins(hand[card_id][0])
        # For n # of matches, create a copy of the n subsequent cards
        # If there are multiple of this card, we create multiple of the subsequent cards
        # i.e. we add as many as there are of this card
        for new_card_id in range(card_id + 1, card_id + matches + 1):
            new_card, current_amount = hand[new_card_id]
            hand[new_card_id] = (new_card, current_amount + hand[card_id][1])

    return sum(amount for _, amount in hand.values())


@component.hook(4, 2, year=2023)
def two(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 4 Part 2 solution."""

    lines = core.load_data(input_stream)

    total = process_deck(parse_scratchcard(line) for line in lines)

    print(f"Total cards collected: {total}", file=output_stream)
