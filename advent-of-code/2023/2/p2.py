import math
import re

# Advent of Code, Day 2


def parse_game_file(filename) -> dict[int, dict[str, int]]:
    games: dict[int, dict[str, int]] = dict()
    with open(filename, "r") as file:
        for line in file:
            game_number, max_colors = parse_game(line)
            games[game_number] = max_colors

    return games


def parse_game(line: str) -> tuple[int, dict[str, int]]:
    game_part, *draws = re.split(":|;|, ", line)
    game_number = int(re.search(r"Game (\d+)", game_part)[1])

    max_colors: dict[str, int] = {"red": 0, "blue": 0, "green": 0}
    for draw in draws:
        num, color = draw.strip().split(" ")
        max_colors[color] = max(max_colors.get(color, 0), int(num))

    return game_number, max_colors


def get_possible_games(
    games: dict[int, dict[str, int]], max_colors: dict[str, int]
) -> list[int]:
    possible_games: list[int] = list()

    for game_number, game_colors in games.items():
        possible = True
        for color, color_number in game_colors.items():
            if color_number > max_colors[color]:
                possible = False
                break
        if possible:
            possible_games.append(game_number)

    return possible_games


# PART 2


def power_of_game(colors: dict[str, int]) -> int:
    return math.prod(colors.values())


def sum_all_powers_of_games(games: dict[int, dict[str, int]]) -> int:
    total = 0

    for game in games.values():
        total += power_of_game(game)

    return total


if __name__ == "__main__":
    input_file = "./advent-of-code/2023/2/p2_input.txt"
    max_colors = {"red": 12, "green": 13, "blue": 14}

    games = parse_game_file(input_file)
    possible_games = get_possible_games(games, max_colors)
    print(sum(possible_games))  # 2447

    # PART 2
    print(sum_all_powers_of_games(games))  # 56322
