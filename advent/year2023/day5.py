"""Solution to Day 5 of AoC."""

import dataclasses
import logging
import string
import typing as t

from advent import core

logger = logging.getLogger(__name__)

# Define component to be imported by main
component = core.Component()

RangeMapping = t.Tuple[int, int, int]


@dataclasses.dataclass(frozen=True)
class Almanac:
    """Data of an almanac input."""

    seeds: t.Iterable[int]

    seed_to_soil: t.Iterable[RangeMapping]
    soil_to_fertilizer: t.Iterable[RangeMapping]
    fertilizer_to_water: t.Iterable[RangeMapping]
    water_to_light: t.Iterable[RangeMapping]
    light_to_temperature: t.Iterable[RangeMapping]
    temperature_to_humidity: t.Iterable[RangeMapping]
    humidity_to_location: t.Iterable[RangeMapping]


def parse_alamanc(lines: t.Iterable[str]) -> Almanac:
    """Parse the textual representation of an almanac."""

    seeds_text, *mappings_lines = lines
    seeds = (
        int(seed_text.strip())
        for seed_text in seeds_text.split("seeds:", maxsplit=1)[1].split()
    )

    mappings: t.Dict[str, t.List[RangeMapping]] = {}

    current = []
    for line in mappings_lines:
        if len(line) > 0:
            if line[0] not in string.digits:
                # header
                # create new list
                mappings[line.split()[0]] = []
                current = mappings[line.split()[0]]
            else:
                # mapping triple
                numbers = [int(number_text) for number_text in line.split()]
                current.append((numbers[0], numbers[1], numbers[2]))

    return Almanac(
        seeds=seeds,
        seed_to_soil=mappings["seed-to-soil"],
        soil_to_fertilizer=mappings["soil-to-fertilizer"],
        fertilizer_to_water=mappings["fertilizer-to-water"],
        water_to_light=mappings["water-to-light"],
        light_to_temperature=mappings["light-to-temperature"],
        temperature_to_humidity=mappings["temperature-to-humidity"],
        humidity_to_location=mappings["humidity-to-location"],
    )


def apply_mapping(value: int, mapping: t.Iterable[RangeMapping]) -> int:
    """Apply a set of range mappings to a number.

    Finds the applicable and returns the result.
    """
    for dest_start, source_start, length in mapping:
        if value in range(source_start, source_start + length):
            return value - source_start + dest_start

    # No ranges applied
    return value


def apply_almanac_mappings(seed: int, almanac: Almanac) -> int:
    """Map a seed to a location using an almanac."""

    # Apply each mapping in order
    mappings = (
        almanac.seed_to_soil,
        almanac.soil_to_fertilizer,
        almanac.fertilizer_to_water,
        almanac.water_to_light,
        almanac.light_to_temperature,
        almanac.temperature_to_humidity,
        almanac.humidity_to_location,
    )

    value = seed
    for mapping in mappings:
        value = apply_mapping(value, mapping)

    return value


@component.hook(5, 1, year=2023)
def one(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 5 Part 1 solution."""

    lines = core.load_data(input_stream)
    almanac = parse_alamanc(lines)

    result = min(apply_almanac_mappings(seed, almanac) for seed in almanac.seeds)

    print(f"Lowest location: {result}", file=output_stream)


# (start, length)
LengthRange = t.Tuple[int, int]


def apply_mapping_to_range(
    value_range: LengthRange, mapping: t.Iterable[RangeMapping]
) -> t.Iterable[LengthRange]:
    """Apply a type-to-type mapping to a range of values.

    Chunks the value range where neccessary.
    For example, if a mapping only applies to half of the value range,
    two chunks are produced.
    """

    source_ranges: t.List[LengthRange] = [value_range]
    destination_ranges: t.List[LengthRange] = []

    for dest_start, source_start, map_length in mapping:
        # e.g. chunk start: 5, chunK_length = 3 (5, 6, 7)
        # dest_start: 2, source_start: 7, length: 5 (7, 8, 9, 10, 11) -> (2, 3, 4, 5, 6)
        destination_ranges.extend(
            [
                chunk
                for chunk_batch in (
                    # If the source start of a mapping segment starts in this chunk,
                    # we bisect the chunk into a mapped and unmapped portion
                    [
                        (chunk_start, source_start - chunk_start),
                        (
                            dest_start,
                            # Mapped range goes up to lower of chunk end and source end
                            (
                                min(
                                    chunk_start + chunk_length,
                                    source_start + map_length,
                                )
                                - source_start
                            ),
                        ),
                    ]
                    for chunk_start, chunk_length in source_ranges
                    if source_start in range(chunk_start, chunk_start + chunk_length)
                )
                for chunk in chunk_batch
            ]
        )

        logger.debug("Current destination ranges: %s", destination_ranges)

        source_ranges = [
            (chunk_start, chunk_length)
            for chunk_start, chunk_length in source_ranges
            if source_start not in range(chunk_start, chunk_start + chunk_length)
        ]

        logger.debug("Current source ranges: %s", source_ranges)

    # Unmapped source ranges are mapped as is
    return destination_ranges + source_ranges


def process_advanced_almanac(almanac: Almanac) -> t.Iterable[LengthRange]:
    """Process an almanac using the advanced method,
    yield location ranges.
    """

    # Apply each mapping in order
    mappings = (
        almanac.seed_to_soil,
        almanac.soil_to_fertilizer,
        almanac.fertilizer_to_water,
        almanac.water_to_light,
        almanac.light_to_temperature,
        almanac.temperature_to_humidity,
        almanac.humidity_to_location,
    )

    seed_values = list(almanac.seeds)

    value_ranges: t.List[LengthRange] = list(zip(seed_values[0::2], seed_values[1::2]))

    logger.debug("Current value ranges: %s", value_ranges)

    for mapping in mappings:
        # Apply the mapping to each of the existing chunks,
        # and flatten the results
        logger.debug("Next mapping: %s", mapping)
        value_ranges = [
            result
            for results in (
                apply_mapping_to_range(value_range, mapping)
                for value_range in value_ranges
            )
            for result in results
        ]

        logger.debug("Current value ranges: %s", value_ranges)

    return value_ranges


@component.hook(5, 2, year=2023)
def two(input_stream: t.TextIO, output_stream: t.TextIO) -> None:
    """Day 5 Part 2 solution."""

    lines = core.load_data(input_stream)
    almanac = parse_alamanc(lines)

    result = min(chunk_start for chunk_start, _ in process_advanced_almanac(almanac))

    print(f"Lowest location: {result}", file=output_stream)
