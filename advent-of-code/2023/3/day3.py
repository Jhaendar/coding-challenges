import math
import re
from typing import Match

NOT_SYMBOLS = "0123456789."


def is_symbol(char: str) -> bool:
    if char in NOT_SYMBOLS:
        return False
    else:
        return True


def contains_symbol(line: str) -> bool:
    for char in line:
        if is_symbol(char):
            return True

    return False


def get_grid_from_input(filename: str) -> list[str]:
    grid: list[str] = list()
    with open(filename, "r") as file:
        for line in file:
            grid.append(line.strip())

    return grid


def get_numbers_from_grid(grid: list[str]) -> int:
    pattern = r"\d+"
    total = 0
    max_y = len(grid)
    for i, line in enumerate(grid):
        for match in re.finditer(pattern, line):
            start, end = match.span()
            valid = False

            if start - 1 > 0:
                start -= 1
            end = end + 1

            # mid
            if contains_symbol(line[start:end]):
                valid = True

            if i - 1 > 0 and contains_symbol(grid[i - 1][start:end]):
                valid = True

            if i + 1 < max_y and contains_symbol(grid[i + 1][start:end]):
                valid = True

            if valid:
                total += int(match.group())

    return total


# PART 2


def get_gear_ratios(grid: list[str]) -> int:
    # Add the product of gear (*) that is adjacent to exactly two numbers.
    # adjacent is all surroundings including top and bottom and diagonals

    pattern_number = r"\d+"
    pattern_gear = r"\*"
    total = 0
    max_y = len(grid)
    for y, line in enumerate(grid):
        for match in re.finditer(pattern_gear, line):
            start, end = match.span()
            if start - 1 > 0:
                start -= 1
            end += 1

            number_matches: list[tuple[int, list[Match[str]]]] = list()

            number_matches.append((y, list(re.finditer(pattern_number, line))))
            if y - 1 >= 0:
                number_matches.append(
                    (y - 1, list(re.finditer(pattern_number, grid[y - 1])))
                )
            if y + 1 < max_y:
                number_matches.append(
                    (y + 1, list(re.finditer(pattern_number, grid[y + 1])))
                )

            adjacent_numbers: set[int] = set()

            for h, numbers in number_matches:
                for number in numbers:
                    number_start, number_end = number.span()
                    number_end -= 1

                    for i in range(start, end):
                        if i in range(*number.span()):
                            adjacent_numbers.add(int(number.group()))

            # only add if the gear is surrounded by exactly two numbers
            if len(adjacent_numbers) == 2:
                total += math.prod(adjacent_numbers)

    return total


if __name__ == "__main__":
    input_file = "./advent-of-code/2023/3/day3_input"
    input_example = "./advent-of-code/2023/3/day3_input_example"

    grid = get_grid_from_input(input_file)
    total = get_numbers_from_grid(grid)
    print(f"Total Part Numbers: {total}")

    # PART 2
    total_gears = get_gear_ratios(grid)
    print(f"Total gear ratios: {total_gears}")
