# Advent of Code, Day 1

import re

number_map = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_coordinates(line: str) -> int:
    """
    Extracts the coordinates from a given string.

    Args:
        line (str): The input string from which the coordinates are extracted.

    Returns:
        int: The extracted coordinates from the input string.

    Raises:
        ValueError: If no digit is found in the input string.

    """
    digits = [char for char in line if char.isdigit()]

    if not digits:
        raise ValueError(f"Input does not contain any digit ({line})")

    coordinates = int(f"{digits[0]}{digits[-1]}")
    return coordinates


def get_coordinates_including_word(line: str) -> int:
    """
    Extracts coordinates from a given string by searching for a pattern that
    includes digits or specific words representing numbers.
    Converts the extracted coordinates into an integer.

    Args:
        line (str): The input string from which coordinates are extracted.

    Returns:
        int: The extracted coordinates as an integer.

    Raises:
        ValueError: If no matches are found in the input string.
    """
    pattern = r"(?=\d|zero|one|two|three|four|five|six|seven|eight|nine)(?=(zero|one|two|three|four|five|six|seven|eight|nine|\d))"  # noqa: E501
    matches = re.findall(pattern, line)

    if not matches:
        raise ValueError(f"Input does not have any digits. ({line=})")

    coordinate_list = [
        number_map.get(match, match) for match in [matches[0], matches[-1]]
    ]
    coordinates = "".join(coordinate_list)

    return int(coordinates)


def process_input(filename: str) -> int:
    total: int = 0
    with open(filename, "r") as file:
        for line in file:
            # sum += get_coordinates(line)
            total += get_coordinates_including_word(line)

    return total


if __name__ == "__main__":
    filename = "advent-of-code/2023/1/p1_input.txt"

    sum = process_input(filename)
    print(sum)
