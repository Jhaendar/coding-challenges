# Advent of Code
# Day 16: The Floor Will Be Lava
from __future__ import annotations

from collections import deque
from typing import Generator, Optional

Paths = dict["Tile", set["Tile"]]


class Tile:
    x: int
    y: int
    type: Optional[str]
    paths: Paths

    def __init__(
        self,
        x: int,
        y: int,
        tile_type: Optional[str] = None,
        paths: Optional[Paths] = None,
    ) -> None:
        self.x = x
        self.y = y
        self.type = tile_type

        if paths is None:
            self.paths = dict()
        else:
            # TODO: Add validations
            self.paths = paths

    def add_path(self, prev_tile: Tile, paths: set[Tile]) -> None:
        self.paths.setdefault(prev_tile, set()).update(paths)

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.x, self.y

    def get_next_coordinates(self) -> dict[str, set[tuple[int, int]]]:
        neighbor_coordinates = self.get_neighbor_coordinates()
        north = neighbor_coordinates["north"]
        south = neighbor_coordinates["south"]
        east = neighbor_coordinates["east"]
        west = neighbor_coordinates["west"]

        next_coordinate: dict[str, set[tuple[int, int]]] = dict()
        if self.type is None or self.type == ".":
            next_coordinate["south"] = {north}
            next_coordinate["north"] = {south}
            next_coordinate["east"] = {west}
            next_coordinate["west"] = {east}
        elif self.type == "|":
            next_coordinate["south"] = {north}
            next_coordinate["north"] = {south}
            next_coordinate["east"] = {north, south}
            next_coordinate["west"] = {north, south}
        elif self.type == "-":
            next_coordinate["north"] = {east, west}
            next_coordinate["south"] = {east, west}
            next_coordinate["west"] = {east}
            next_coordinate["east"] = {west}
        elif self.type == "\\":
            next_coordinate["north"] = {east}
            next_coordinate["south"] = {west}
            next_coordinate["west"] = {south}
            next_coordinate["east"] = {north}
        elif self.type == "/":
            next_coordinate["north"] = {west}
            next_coordinate["south"] = {east}
            next_coordinate["west"] = {north}
            next_coordinate["east"] = {south}
        else:
            raise ValueError(f"INVALID tyle type: {self.type}")

        return next_coordinate

    def get_neighbor_coordinates(self) -> dict[str, tuple[int, int]]:
        neighbor_coordinates: dict[str, tuple[int, int]] = {
            "north": (self.x, self.y - 1),
            "south": (self.x, self.y + 1),
            "west": (self.x - 1, self.y),
            "east": (self.x + 1, self.y),
        }

        return neighbor_coordinates

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return False
        return self.x == other.x and self.y == other.y and self.type == other.type

    def __repr__(self) -> str:
        return f"Point{self.x, self.y, self.type}"


class Grid:
    grid: list[list[str]]
    max_x: int
    max_y: int
    tiles: dict[tuple[int, int], Tile]

    def __init__(self, grid: list[list[str]]) -> None:
        self.grid = grid
        self.max_y = len(grid)
        self.max_x = len(grid[0])
        self.tiles = dict()
        self.generate_tiles_from_grid(grid)

    def generate_tiles_from_grid(self, grid: list[list[str]]) -> None:
        for y, line in enumerate(grid):
            for x, tile_type in enumerate(line):
                tile = self.tiles.setdefault((x, y), Tile(x, y))
                tile.type = tile_type
                self.add_neighbors(tile)

    def add_neighbors(self, tile: Tile):
        neighbor_coordinates = tile.get_neighbor_coordinates()
        next_coordinates = tile.get_next_coordinates()

        for direction in {"north", "south", "east", "west"}:
            # From
            fx, fy = neighbor_coordinates[direction]
            if fx < 0 or fx >= self.max_x or fy < 0 or fy >= self.max_y:
                continue

            neighbor_tile = self.tiles.setdefault((fx, fy), Tile(fx, fy))

            # Destination
            next_paths: set[Tile] = set()
            for nx, ny in next_coordinates[direction]:
                if nx >= 0 and nx < self.max_x and ny >= 0 and ny < self.max_y:
                    next_paths.add(self.tiles.setdefault((nx, ny), Tile(nx, ny)))

            tile.add_path(neighbor_tile, next_paths)

    @property
    def shape(self) -> tuple[int, int]:
        """Return (max_x, max_y)

        Returns:
            tuple[int,int]: (max_x, max_y)
        """
        return self.max_x, self.max_y

    def __getitem__(self, key: tuple[int, int]) -> Tile:
        x, y = key
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            raise KeyError(f"Invalid key: {key}")
        return self.tiles[(x, y)]


def parse_file(filename: str) -> Generator[str, None, None]:
    with open(filename, "r") as file:
        for line in file:
            yield line.strip()


def parse_grid(filename: str) -> Grid:
    grid: list[list[str]] = list()
    for line in parse_file(filename):
        grid.append(list(line))

    return Grid(grid)


DIRECTION_PREV_DELTAS = {
    "north": (0, -1),
    "south": (0, 1),
    "east": (-1, 0),
    "west": (1, 0),
}
DIRECTION_NEXT_DELTAS = {
    "north": (0, 1),
    "south": (0, -1),
    "east": (1, 0),
    "west": (-1, 0),
}


def generate_false_start(tile: Tile, direction: str, grid: Grid) -> Tile:
    x, y = tile.coordinates
    dx, dy = DIRECTION_PREV_DELTAS[direction]
    false_start_tile = Tile(x + dx, y + dy)

    ndx, ndy = DIRECTION_NEXT_DELTAS[direction]
    tile.add_path(false_start_tile, {grid[x + ndx, y + ndy]})

    return false_start_tile


def part_one_solution(input_file: str):
    grid = parse_grid(input_file)

    # special starting tile!
    path = explore_path(grid[0, 0], "east", grid)

    print(len(path))


def explore_path(start: Tile, direction: str, grid: Grid):
    false_start_tile = generate_false_start(start, direction, grid)

    current_path: set[tuple[Tile, Tile]] = set()
    visited: set[Tile] = set()

    paths_to_explore: deque[tuple[Tile, Tile]] = deque()
    paths_to_explore.append((false_start_tile, start))

    while paths_to_explore:
        prev_tile, current_tile = paths_to_explore.pop()

        if (prev_tile, current_tile) in current_path:
            continue

        for next_tile in current_tile.paths[prev_tile]:
            paths_to_explore.append((current_tile, next_tile))

        current_path.add((prev_tile, current_tile))
        visited.add(current_tile)

    return visited


def part_two_solution(input_file):
    grid = parse_grid(input_file)
    max_x, max_y = grid.shape
    x = 0
    y = 0
    direction = "east"
    max_energized = 0
    for y in range(max_y):
        path = explore_path(grid[x, y], direction, grid)

        max_energized = max(max_energized, len(path))

    direction = "west"
    for y in range(max_y):
        path = explore_path(grid[max_x - 1, y], direction, grid)

        max_energized = max(max_energized, len(path))

    direction = "north"
    for x in range(max_x):
        path = explore_path(grid[x, 0], direction, grid)

        max_energized = max(max_energized, len(path))

    direction = "south"
    for x in range(max_x):
        path = explore_path(grid[x, max_y - 1], direction, grid)

        max_energized = max(max_energized, len(path))

    print(max_energized)


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/16/day16_input_example")
    input_files.append("./advent-of-code/2023/16/day16_input")

    # Answers:

    for input_file in input_files:
        print(f"\nUsing input file: {input_file}")
        part_one_solution(input_file)
        part_two_solution(input_file)
