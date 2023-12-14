# Advent of Code
# Day 14: Parabolic Reflector Dish

Grid = list[list[str]]


def parse_file(filename: str) -> Grid:
    # make a transposed grid
    grid: Grid = list()
    transposed_grid: Grid = list()
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if len(grid) == 0:
                grid = [list() for x in range(len(line))]

            for x, e in enumerate(line):
                grid[x].append(e)

        for row in grid:
            transposed_grid.append(row)

    return transposed_grid


def move_rocks_to_left(grid: Grid):
    for line in grid:
        free_spot: set[int] = set()

        for x, tile in enumerate(line):
            if tile == ".":
                free_spot.add(x)

            if tile == "#":
                free_spot = set()

            if tile == "O" and free_spot:
                current = min(free_spot)
                free_spot.remove(current)

                line[x], line[current] = line[current], line[x]
                free_spot.add(x)

    return grid


def calculate_total_load(grid: Grid) -> int:
    total = 0
    max_x = len(grid[0])
    for y, line in enumerate(grid):
        for x, tile in enumerate(line):
            if tile == "O":
                total += max_x - x

    return total


def part_one_solution(input_file: str):
    grid = parse_file(input_file)
    grid = move_rocks_to_left(grid)

    total = calculate_total_load(grid)
    print(total)


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/14/day14_input_example")
    input_files.append("./advent-of-code/2023/14/day14_input")

    # Answers:

    for input_file in input_files:
        print(f"\nUsing input file: {input_file}")
        part_one_solution(input_file)
