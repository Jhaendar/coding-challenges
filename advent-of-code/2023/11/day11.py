from itertools import combinations
from typing import Iterable, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


GalaxyMap = list[Point]
Pair = tuple[Point, Point]


def parse_file(filename: str) -> tuple[list[Point], set[int], set[int]]:
    with open(filename, "r") as file:
        galaxy_points: list[Point] = list()
        not_empty_cols: set[int] = set()
        empty_rows: set[int] = set()

        for y, line in enumerate(file):
            empty_row = True
            for x, point in enumerate(line):
                if point == "#":
                    galaxy_points.append(Point(x, y))
                    not_empty_cols.add(x)
                    empty_row = False

            if empty_row:
                empty_rows.add(y)

        # Calculate empty columsn from not_empty columns
        empty_cols = {
            x for x in range(max(not_empty_cols)) if x not in not_empty_cols
        }

    return galaxy_points, empty_rows, empty_cols


def calculate_manhattan_distance(
    start: Point, end: Point, x_offset: int, y_offset: int
) -> int:
    return abs(start.x - end.x) + abs(start.y - end.y) + x_offset + y_offset


def calculate_shortest_paths(
    pairs: Iterable[Pair],
    empty_rows: set[int],
    empty_cols: set[int],
    expansion: int,
) -> Iterable[int]:
    for pair in pairs:
        if pair[0].x < pair[1].x:
            x_range = range(pair[0].x, pair[1].x)
        else:
            x_range = range(pair[1].x, pair[0].x)

        if pair[0].y < pair[1].y:
            y_range = range(pair[0].y, pair[1].y)
        else:
            y_range = range(pair[1].y, pair[0].y)

        x_offset = sum(x in empty_cols for x in x_range) * (expansion - 1)
        y_offset = sum(y in empty_rows for y in y_range) * (expansion - 1)

        yield calculate_manhattan_distance(
            pair[0], pair[1], x_offset, y_offset
        )


def calculate_total_shortest_paths(
    galaxy_points: list[Point],
    empty_rows: set[int],
    empty_cols: set[int],
    expansion: int,
) -> int:
    pairs = combinations(galaxy_points, 2)

    distances = calculate_shortest_paths(
        pairs, empty_rows, empty_cols, expansion
    )
    return sum(distances)


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/11/day11_input_example")
    input_files.append("./advent-of-code/2023/11/day11_input")

    # Answers:

    for input_file in input_files:
        print(f"\nUsing input file: {input_file}")

        expansion = 1_000_000

        galaxy_points, empty_rows, empty_cols = parse_file(input_file)

        total = calculate_total_shortest_paths(
            galaxy_points, empty_rows, empty_cols, expansion
        )

        print(f"{total=}")
