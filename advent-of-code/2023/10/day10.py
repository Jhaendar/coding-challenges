from __future__ import annotations

from collections import deque
from typing import Iterable, Optional


class Point:
    def __init__(
        self,
        x: int,
        y: int,
        neighbors: Optional[set[Point]] = None,
        direction: Optional[str] = None,
    ):
        self.x: int = x
        self.y: int = y
        if neighbors is None:
            neighbors = set()

        self.neighbors: set[Point] = neighbors

        if direction is None:
            direction = "."

        self.direction: str = direction

    @property
    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self):
        return f"P({self.x}, {self.y}, {self.direction})"


Maze = dict[tuple[int, int], Point]

maze_character_map: dict[str, str] = {  # NSWE
    "|": "NS",
    "-": "WE",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
}

direction_map: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "S": (0, 1),
    "W": (-1, 0),
    "E": (1, 0),
}


def get_neighbors(point: Point) -> set[tuple[int, int]]:
    neighbors: set[tuple[int, int]] = set()

    for direction in point.direction:
        dx, dy = direction_map[direction]
        neighbors.add((point.x + dx, point.y + dy))

    return neighbors


def add_node_neighbors(start: Point, maze: Maze):
    x, y = start.coords
    directions: set[str] = set()

    for direction, delta in direction_map.items():
        dx, dy = delta
        coords = (x + dx, y + dy)

        if coords in maze and start in maze[coords].neighbors:
            start.neighbors.add(maze[coords])
            directions.add(direction)

    start.direction = "".join(directions)


def parse_file(filename: str) -> tuple[Point, Maze]:
    maze: Maze = dict()
    start: Optional[Point] = None

    with open(filename, "r") as file:
        for y, line in enumerate(file):
            for x, tile in enumerate(line):
                if tile == "S":
                    start = maze.setdefault((x, y), Point(x, y))

                if tile in maze_character_map:
                    point = maze.setdefault((x, y), Point(x, y))

                    point.direction = maze_character_map[tile]

                    for neighbor in get_neighbors(point):
                        neighbor_point = maze.setdefault(
                            neighbor, Point(*neighbor)
                        )

                        point.neighbors.add(neighbor_point)

    if start is None:
        raise ValueError("No starting position Found!")

    add_node_neighbors(start, maze)
    return start, maze


def calculate_distances(
    start: Point, maze: Maze
) -> tuple[dict[tuple[int, int], int], set[Point]]:
    distances: dict[tuple[int, int], int] = dict()

    q: deque[Point] = deque([start])
    distances[start.coords] = 0
    visited: set[Point] = set([start])

    while q:
        current = q.popleft()
        visited.add(current)
        distance = distances[current.coords] + 1

        for neighbor in current.neighbors:
            if neighbor not in visited or distance < distances.get(
                neighbor.coords, float("inf")
            ):
                q.append(neighbor)
                distances[neighbor.coords] = distance

    return distances, visited


def group_by_y(points: Iterable[Point]) -> dict[int, list[Point]]:
    grouped: dict[int, list[Point]] = dict()

    # group
    for point in points:
        group = grouped.setdefault(point.y, list())
        if point.direction != "WE":
            group.append(point)

    # sort
    for y in grouped:
        grouped[y].sort(key=lambda p: p.x)

    return grouped


def have_odd_walls(norths: int, souths: int) -> bool:
    return min(norths, souths) % 2 == 1


def calculate_enclosed_area(grouped_vertices: dict[int, list[Point]]) -> int:
    area = 0

    for vertices in grouped_vertices.values():
        norths = 0
        souths = 0

        for i in range(len(vertices) - 1):
            left = vertices[i]
            right = vertices[i + 1]

            norths += left.direction.count("N")
            souths += left.direction.count("S")

            diff = right.x - left.x - 1

            if (
                "W" not in right.direction
                and have_odd_walls(norths, souths)
                and diff > 0
            ):
                area += diff

    return area


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/10/day10_input_example")
    input_files.append("./advent-of-code/2023/10/day10_input_example_2")
    input_files.append("./advent-of-code/2023/10/day10_input_example_3")
    input_files.append("./advent-of-code/2023/10/day10_input_example_4")
    input_files.append("./advent-of-code/2023/10/day10_input")

    # Answers:

    for input_file in input_files:
        print(f"\nUsing input file: {input_file}")

        start, maze = parse_file(input_file)
        distances, vertices = calculate_distances(start, maze)
        print(f"{start=}")

        # Part 1
        max_distance = max(distances.values())
        print(f"{max_distance=}")

        # Part 2
        grouped = group_by_y(vertices)
        area = calculate_enclosed_area(grouped_vertices=grouped)
        print(f"{area=}")
