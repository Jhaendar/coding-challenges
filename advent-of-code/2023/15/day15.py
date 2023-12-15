from functools import lru_cache
from typing import Generator

CHUNK_SIZE = 1024


def parse_file(filename: str) -> Generator[str, None, None]:
    leftover = ""
    with open(filename, "r") as file:
        while chunk := file.read(CHUNK_SIZE):
            sequence = chunk.strip().split(",")
            sequence[0] = leftover + sequence[0]
            leftover = sequence.pop()

            for step in sequence:
                yield step

        else:
            yield leftover


@lru_cache
def calculate_hash_value(string: str) -> int:
    hash_value = 0
    base = 17
    mod = 256
    for i, character in enumerate(string, start=1):
        hash_value = ((hash_value + ord(character)) * base) % mod

    return hash_value


def part_one_solution(input_file: str):
    total = 0
    for sequence in parse_file(input_file):
        hash_value = calculate_hash_value(sequence)
        total += hash_value

    print(total)


def part_two_solution(input_file: str):
    boxes: dict[int, list[tuple[str, int]]] = dict()
    box_labels: dict[int, dict[str, int]] = dict()

    for sequence in parse_file(input_file):
        # remove operation
        if sequence[-1] == "-":
            sequence = sequence[:-1]
            hash_value = calculate_hash_value(sequence)

            # ensure list and dict are initialized
            boxes.setdefault(hash_value, list())
            box_labels.setdefault(hash_value, dict())

            # remove
            if sequence in box_labels[hash_value]:
                old_value = (sequence, box_labels[hash_value][sequence])
                boxes[hash_value].remove(old_value)
                box_labels[hash_value].pop(sequence)

        # add operation
        else:
            sequence, focal_length_str = sequence.split("=")
            focal_length = int(focal_length_str)
            hash_value = calculate_hash_value(sequence)

            value = (sequence, focal_length)

            # ensure list and dict are initialized
            boxes.setdefault(hash_value, list())
            box_labels.setdefault(hash_value, dict())

            # replace
            if sequence in box_labels[hash_value]:
                old_value = (sequence, box_labels[hash_value][sequence])

                index = boxes[hash_value].index(old_value)
                boxes[hash_value][index] = value
                box_labels[hash_value][sequence] = focal_length

            else:  # add new
                boxes[hash_value].append(value)
                box_labels[hash_value][sequence] = focal_length

    total = 0
    for box_number, box in boxes.items():
        for slot, lens_info in enumerate(box, start=1):
            label, focal_length = lens_info
            v = (box_number + 1) * (slot) * focal_length
            total += v

    print(total)


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/15/day15_input_example")
    input_files.append("./advent-of-code/2023/15/day15_input")

    # Answers:

    for input_file in input_files:
        print(f"\nUsing input file: {input_file}")
        part_one_solution(input_file)
        part_two_solution(input_file)
