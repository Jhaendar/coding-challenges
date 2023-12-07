import math
from typing import Optional


def parse_file(filename: str, part: Optional[int] = 2) -> dict[str, list[int]]:
    times: list[int] = list()
    records: list[int] = list()

    with open(filename, "r") as file:
        if part == 1:
            times = [int(x) for x in file.readline().split()[1:]]
            records = [int(x) for x in file.readline().split()[1:]]
        if part == 2:
            times = [int("".join([x for x in file.readline().split()[1:]]))]
            records = [int("".join([x for x in file.readline().split()[1:]]))]

    parsed_info = {"times": times, "records": records}
    return parsed_info


def get_time_range(time: int, record: int) -> range:
    # use quadratic formula
    discriminant = ((time**2) - 4 * 1 * record) ** 0.5
    x1 = math.ceil((time + discriminant) / 2)
    x2 = int((time - discriminant) / 2)

    solution_range = range(x2, x1 - 1)
    return solution_range


def find_ways_to_win(times: list[int], records: list[int]) -> list[int]:
    solutions: list[int] = list()
    for time, record in zip(times, records):
        num_solution = len(get_time_range(time, record))
        solutions.append(num_solution)

    return solutions


if __name__ == "__main__":
    input_file = "./advent-of-code/2023/6/day6_input"
    input_example = "./advent-of-code/2023/6/day6_input_example"

    parsed_info = parse_file(input_file, part=2)
    # parsed_info = parse_file(input_example, part=2)
    times = parsed_info["times"]
    records = parsed_info["records"]
    solutions = find_ways_to_win(times, records)
    print(solutions)
    print(math.prod(solutions))
