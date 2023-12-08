import itertools
import math
import re

Network = dict[str, dict[str, str]]


def parse_file(filename: str) -> tuple[list[str], str, Network]:
    network: Network = dict()
    starts: list[str] = list()

    with open(filename, "r") as file:
        directions = file.readline().strip()
        next(file)

        for line in file:
            line = line.replace("(", "").replace(")", "").strip()
            node, left, right = [str(x) for x in re.split(" = |, ", line)]

            network[node] = {"L": left, "R": right}

            if node[-1] == "A":
                starts.append(node)

        return starts, directions, network


def find_node(
    start: str, target: str, directions: str, network: Network
) -> int:
    current = start
    steps = 0
    directions_cycle = itertools.cycle(directions)

    while current != target:
        direction = next(directions_cycle)

        if current not in network:
            raise KeyError(f"{current} not in network!")

        current = network[current][direction]

        steps += 1

    return steps


# PART 2
def find_all_node(starts: list[str], directions: str, network: Network) -> int:
    loops: list[int] = list()

    for start in starts:
        current = start
        steps = 0
        directions_cycle = itertools.cycle(directions)
        while current.endswith("Z") is False:
            direction = next(directions_cycle)
            current = network[current][direction]

            steps += 1

        loops.append(steps)
    return math.lcm(*loops)


if __name__ == "__main__":
    input_file = "./advent-of-code/2023/8/day8_input"
    input_example = "./advent-of-code/2023/8/day8_input_example"
    input_example_2 = "./advent-of-code/2023/8/day8_input_example_2"

    files = list()
    files.append(input_file)
    files.append(input_example)
    files.append(input_example_2)

    for file in files:
        print(f"Processing file: {file}")
        starts, directions, network = parse_file(file)

        steps = find_node("AAA", "ZZZ", directions, network)
        print(f"Part 1: {steps}")

        steps = find_all_node(starts, directions, network)
        print(f"Part 2: {steps}")
