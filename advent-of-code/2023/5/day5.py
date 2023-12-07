# Advent of Code, Day 5
from collections import namedtuple

Mapping = namedtuple("Mapping", ["source", "dest"])
MappingResult = namedtuple("MappingResult", ["mapped", "unmapped"])
MappingsList = list[Mapping]


def parse_file(
    filename: str, part: int = 2
) -> tuple[list[range], list[MappingsList]]:
    seeds: list[range] = list()
    mappings: list[MappingsList] = list()
    with open(filename, "r") as file:
        seed_line = file.readline()[7:].split()

        if part == 2:
            # Part 2
            for i in range(0, len(seed_line), 2):
                start = int(seed_line[i])
                stop = start + int(seed_line[i + 1])
                seed_range = range(start, stop)
                seeds.append(seed_range)
        else:
            # PART 1
            seeds = [range(int(x), int(x) + 1) for x in seed_line]

        current_mapping: MappingsList = list()
        for line in file:
            if line == "\n":
                continue

            if ":" in line:
                mappings.append(list())
                current_mapping = mappings[-1]
                continue

            dest, source, step = [int(x) for x in line.split()]
            dest_range = range(dest, dest + step)
            source_range = range(source, source + step)

            mapping = Mapping(source_range, dest_range)

            current_mapping.append(mapping)

    return seeds, mappings


def map_range(seed: range, mapping: Mapping) -> MappingResult:
    mapped: list[range] = list()
    unmapped: list[range] = list()

    source_range = mapping.source
    dest_range = mapping.dest
    difference = dest_range.start - source_range.start

    mapped_range_start = max(seed.start, source_range.start)
    mapped_range_stop = min(seed.stop, source_range.stop)

    # transform to destination range
    if mapped_range_start <= mapped_range_stop:
        mapped_range = range(
            mapped_range_start + difference, mapped_range_stop + difference
        )
        mapped.append(mapped_range)

    # check for unmapped range
    left = range(seed.start, min(seed.stop, source_range.start))
    right = range(max(seed.start, source_range.stop), seed.stop)
    # print(f"{left=}, {right=}")
    unmapped = [x for x in [left, right] if x]

    return MappingResult(mapped, unmapped)


def follow_the_map(
    seeds: list[range], mappings_list: list[MappingsList]
) -> list[range]:
    # print(seeds)
    seeds_map_result = [MappingResult(list(), [seed]) for seed in seeds]
    # print(f"{seeds_map_result=}")
    for mappings in mappings_list:
        # print("-new stage")
        for mapping in mappings:
            # print("--new map")
            for i, seed in enumerate(seeds_map_result):
                # print(f"\n---{seed=}")
                # print(f"---{mapping=}")
                unmapped_list: list[range] = list()
                for unmapped_seed in seed.unmapped:
                    # print(f"----{unmapped_seed=}")
                    mapped, unmapped = map_range(unmapped_seed, mapping)
                    # print(f"----{mapped=}")
                    if mapped:
                        seed.mapped.extend(mapped)
                    unmapped_list.extend(unmapped)

                seeds_map_result[i] = MappingResult(seed.mapped, unmapped_list)
                # print(f"---new seed: {seeds_map_result[i]}")

        # print(f"\n-old seed map: {seeds_map_result}")
        seeds_map_result = [
            MappingResult(list(), x.unmapped + x.mapped)
            for x in seeds_map_result
        ]
        # print(f"-new seed map: {seeds_map_result}")
    # print(seeds_map_result)
    final_map: list[range] = list()
    for seed in seeds_map_result:
        final_map.extend(seed.unmapped)

    return final_map


if __name__ == "__main__":
    input_file = "./advent-of-code/2023/5/day5_input"
    input_example = "./advent-of-code/2023/5/day5_input_example"

    # PART 1
    seeds, mappings_list = parse_file(input_file, part=1)
    locations = follow_the_map(seeds, mappings_list)
    print(min([x.start for x in locations]))

    # PART 2
    seeds, mappings_list = parse_file(input_file)
    locations = follow_the_map(seeds, mappings_list)
    print(min([x.start for x in locations]))
