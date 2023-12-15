# Advent of Code
# Day 14: Parabolic Reflector Dish

from collections import deque
from functools import lru_cache

Grid = list[list[str]]

CycleDirection = ["north", "west", "south", "east"]


def parse_file(filename: str) -> Grid:
    grid: Grid = list()
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            grid.append(list(line))

    return grid


def get_ranges(direction: str, height: int, width: int) -> tuple[range, range]:
    if direction == "east":
        i_range = range(height)
        j_range = range(width - 1, -1, -1)
    elif direction == "west":
        i_range = range(height)
        j_range = range(width)
    elif direction == "north":
        i_range = range(height - 1, -1, -1)
        j_range = range(width)
    elif direction == "south":
        i_range = range(width)
        j_range = range(height - 1, -1, -1)
    else:
        raise KeyError("INVALID DIRECTION")

    return i_range, j_range


def grid_to_string(grid: Grid) -> str:
    grid_str = "".join(["".join(line) for line in grid])

    return grid_str


def string_to_grid(grid_str: str, max_y: int, max_x: int) -> Grid:
    grid: Grid = list()
    for i in range(max_y):
        start = i * max_x
        grid.append(list(grid_str[start : start + max_x]))

    return grid


@lru_cache
def move_rocks(grid_str: str, direction: str, max_y: int, max_x: int) -> str:
    grid = string_to_grid(grid_str, max_y, max_x)
    max_y = len(grid)
    max_x = len(grid[0])
    free_spot: deque[tuple[int, int]] = deque()

    i_range, j_range = get_ranges(direction, max_y, max_x)
    for i in i_range:
        free_spot = deque()
        for j in j_range:
            if direction in {"east", "west"}:
                y, x = i, j
            elif direction in {"north", "south"}:
                y, x = j, i
            else:
                raise KeyError(f"Invalid direction: {direction}")

            tile = grid[y][x]

            if tile == ".":
                free_spot.append((y, x))
            if tile == "#":
                free_spot = deque()

            if tile == "O" and free_spot:
                free_spot_y, free_spot_x = free_spot.popleft()
                free_spot.append((y, x))

                grid[y][x], grid[free_spot_y][free_spot_x] = (
                    grid[free_spot_y][free_spot_x],
                    grid[y][x],
                )

    return grid_to_string(grid)


def move_rocks_wrapper(grid: Grid, direction: str) -> Grid:
    max_y = len(grid)
    max_x = len(grid[0])

    grid_str = grid_to_string(grid)

    new_grid_str = move_rocks(grid_str, direction, max_y, max_x)

    new_grid = string_to_grid(new_grid_str, max_y, max_x)

    return new_grid


def calculate_total_load(grid: Grid) -> int:
    total = 0
    max_y = len(grid)
    max_x = len(grid[0])
    for i in range(max_y):
        for j in range(max_x):
            if grid[i][j] == "O":
                total += max_y - i

    return total


def print_grid(grid: Grid):
    for line in grid:
        print("".join(line))


def spin_cycle(grid: Grid, cycles: int):
    encountered_grids: dict[str, int] = dict()
    cycle = 0
    while cycle < cycles:
        for direction in CycleDirection:
            grid = move_rocks_wrapper(grid, direction)

        grid_str = grid_to_string(grid)

        if grid_str in encountered_grids:
            needed = cycles - cycle
            grid_cycle = cycle - encountered_grids[grid_str]

            if needed > grid_cycle:
                cycle += needed - (needed % grid_cycle)
        else:
            encountered_grids[grid_str] = cycle
        cycle += 1

    return grid


def part_one_solution(input_file: str):
    grid = parse_file(input_file)
    grid = move_rocks_wrapper(grid, "north")

    total = calculate_total_load(grid)
    print(total)


def part_two_solution(input_file: str):
    grid = parse_file(input_file)

    grid = spin_cycle(grid, 1000000000)
    total = calculate_total_load(grid)
    print(total)


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/14/day14_input_example")
    input_files.append("./advent-of-code/2023/14/day14_input")

    # Answers:

    for input_file in input_files:
        print(f"Input File: {input_file}")
        part_one_solution(input_file)
        part_two_solution(input_file)
