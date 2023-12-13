from __future__ import annotations

import numpy
import math
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from time import time_ns, sleep
from functools import wraps, cache, cached_property, cmp_to_key
from copy import copy


# === Useful Functions === #


def splitlines(data: str, fun=lambda x: x) -> List[str]:
    return [fun(line) for line in data.splitlines() if line]


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time_ns()
        result = f(*args, **kwargs)
        delta = (time_ns() - start) / 1000000.0
        print(f'Elapsed time of {f.__name__}: {delta} ms')
        return result

    return wrapper


# === Types === #


@dataclass
class Input:
    data: str
    patterns: List[List[str]]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    patterns = []
    lines = []
    for line in data.splitlines():
        if not line:
            patterns.append(lines)
            lines = []
        else:
            lines.append(line)
    if lines:
        patterns.append(lines)
    return Input(data, patterns)


def parse_input_1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input_2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def find_horizontal_reflection(lines: List[str], smudges: int = 0) -> int:
    cols = len(lines[0])
    rows = len(lines)
    for row in range(1, rows):
        height = min(row, rows - row)
        wrongs = 0
        for right_y in range(row, row + height):
            left_y = row - (right_y - row) - 1
            for x in range(0, cols):
                if lines[right_y][x] != lines[left_y][x]:
                    wrongs += 1
                    if wrongs > smudges:
                        break
        if wrongs == smudges:
            return row
    return 0


def find_vertical_reflection(lines: List[str], smudges: int = 0) -> int:
    cols = len(lines[0])
    rows = len(lines)
    for col in range(1, cols):
        width = min(col, cols - col)
        wrongs = 0
        for right_x in range(col, col + width):
            left_x = col - (right_x - col) - 1
            for y in range(0, rows):
                if lines[y][right_x] != lines[y][left_x]:
                    wrongs += 1
                    if wrongs > smudges:
                        break
        if wrongs == smudges:
            return col
    return 0


def solution(input: Input, smudges: int) -> int:
    sum = 0
    for pattern in input.patterns:
        rows = find_horizontal_reflection(pattern, smudges)
        cols = find_vertical_reflection(pattern, smudges)
        sum += rows * 100 + cols
    return sum


@timer
def solve_1(input: Input) -> Optional[int]:
    return solution(input, 0)


@timer
def solve_2(input: Input) -> Optional[int]:
    return solution(input, 1)


# ==== Solutions with test data ==== #


test_data_1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
test_answer_1 = 405

test_data_2 = test_data_1
test_answer_2 = 400


# ==== Template for running solutions ==== #


@timer
def main():
    start = time_ns()
    filename = 'input.txt'
    with open(filename, 'r') as f:
        input = f.read()
        delta = (time_ns() - start) / 1000000.0
        print(f'Elapsed time of reading file: {delta} ms')

        for number in range(1, 3):
            func = globals()[f'solve_{number}']
            parse = globals()[f'parse_input_{number}']

            slv = func(parse(globals()[f'test_data_{number}']))
            answer = globals()[f'test_answer_{number}']
            if slv == answer:
                print(f'\nSolution {number} - Test has passed\n')
            else:
                print(f'\nSolution {number} - Test has failed.')
                print(f'Correct: {answer}\nBut got: {slv}\n')
                continue

            slv = func(parse(input))
            if slv is not None:
                print(f'\nSolution {number} - The answer is {slv}\n')


if __name__ == '__main__':
    main()
