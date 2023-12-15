# Advent of Code
# Day 14: Parabolic Reflector Dish

from collections import deque
from typing import Generator

Grid = list[list[str]]


def parse_file(filename: str) -> Grid:
    # make a transposed grid
    grid: Grid = list()
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            grid.append(list(line))

    return grid


def get_ranges(
    direction: str, height: int, width: int
) -> Generator[tuple[int, int], None, None]:
    if direction == "east":
        i_range = range(height)
        j_range = range(width)
    elif direction == "west":
        i_range = range(height - 1, -1, -1)
        j_range = range(width - 1, -1, -1)
    elif direction == "south":
        i_range = range(height)
        j_range = range(width)
    elif direction == "north":
        i_range = range(height - 1, -1, -1)
        j_range = range(width - 1, -1, -1)
    else:
        raise KeyError("INVALID DIRECTION")

    for i in i_range:
        for j in j_range:
            if direction in {"east", "west"}:
                yield i, j
            elif direction in {"north", "south"}:
                yield j, i


def move_rocks(grid: Grid, direction: str):
    max_y = len(grid)
    max_x = len(grid[0])
    i_range, j_range = get_ranges(direction, max_y, max_x)
    print(i_range, j_range)
    for i in i_range:
        free_spot: deque[int] = deque()
        for j in j_range:
            tile = grid[i][j]

            if tile == ".":
                free_spot.append(j)
            if tile == "#":
                free_spot = deque()

            if tile == "O" and free_spot:
                current = free_spot.popleft()
                free_spot.append(j)

                grid[i][j], grid[i][current] = grid[i][current], grid[i][j]

    return grid


def test(direction, y, x):
    for i, j in get_ranges(direction, y, x):
        print(i, j)


# def spin_cycle(grid: Grid, cycles: int):
#     cycle_direction = ""


def calculate_total_load(grid: Grid) -> int:
    total = 0
    max_y = len(grid)
    max_x = len(grid[0])
    i_range, j_range = get_ranges("north", max_y, max_x)

    for i in i_range:
        for j in j_range:
            if grid[i][j] == "O":
                total += max_y - j

    return total


def print_grid(grid: Grid):
    for line in grid:
        print("".join(line))


def part_one_solution(input_file: str):
    grid = parse_file(input_file)
    grid = move_rocks(grid, "north")
    print_grid(grid)
    total = calculate_total_load(grid)
    print(total)


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/14/day14_input_example")
    # input_files.append("./advent-of-code/2023/14/day14_input")

    # Answers:

    for input_file in input_files:
        print(f"\nUsing input file: {input_file}")
        test("north", 4, 3)

        # part_one_solution(input_file)
