import math
from typing import Generator

InputGenerator = Generator[list[int], None, None]


def input_line_generator(filename: str) -> InputGenerator:
    with open(filename, "r") as file:
        for line in file:
            yield [int(x) for x in line.strip().split()]


def get_binomial_coeffs(n: int) -> list[int]:
    return [((-1) ** k) * math.comb(n, k) for k in range(n + 1)]


def extrapolate_next_value(data: list[int]) -> int:
    coeffs = 0
    for i in range(1, len(data)):
        binomial_coeffs = get_binomial_coeffs(i)
        coeffs += sum(a * b for a, b in zip(binomial_coeffs, data))
    return data[0] + coeffs


def extrapolate_diffs(data: list[int]) -> int:
    coeffs = 0
    while any(data):
        coeffs += data[-1]
        data = [data[i + 1] - data[i] for i in range(len(data) - 1)]
    return coeffs


def extrapolate_all_next_values(input_gen: InputGenerator) -> list[int]:
    return [extrapolate_next_value(data) for data in input_gen]


def extrapolate_all_prev_values(input_gen: InputGenerator) -> list[int]:
    return [extrapolate_next_value(data[::-1]) for data in input_gen]


if __name__ == "__main__":
    input_files: list[str] = list()
    input_files.append("./advent-of-code/2023/9/day9_input_example")
    input_files.append("./advent-of-code/2023/9/day9_input")

    # Answers:
    # PART 1: 114, 1681758908

    for input_file in input_files:
        print(f"\nUsing input file: {input_file}")

        # PART 1
        input_gen = input_line_generator(input_file)
        # prev_values = extrapolate_all_prev_values(input_gen)
        prev_values = [extrapolate_diffs(line) for line in input_gen]
        print(f"sum={sum(prev_values)}")

        # PART 2
        input_gen = input_line_generator(input_file)
        # next_values = extrapolate_all_next_values(input_gen)
        next_values = [extrapolate_diffs(line[::-1]) for line in input_gen]
        print(f"sum={sum(next_values)}")
