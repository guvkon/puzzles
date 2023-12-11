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
    lines: List[str]
    expanded: List[str]
    galaxies: List[Tuple[int, int]]


# === Input parsing === #


def has_galaxies(lines: List[str], x: int) -> bool:
    for y in range(0, len(lines)):
        point = lines[y][x]
        if point == '#':
            return True
    return False


def expand_universe(lines: List[str]) -> List[str]:
    expanded = []
    empty_line = '.' * len(lines[0])
    expanded_line = 'E' * len(lines[0])
    for line in lines:
        if line == empty_line:
            expanded.append(expanded_line)
        else:
            expanded.append(line)
    for x in range(len(lines[0]) - 1, -1, -1):
        if has_galaxies(lines, x):
            continue
        for y in range(0, len(expanded)):
            point = 'E'
            expanded[y] = expanded[y][0:x] + point + expanded[y][x + 1:]
    return expanded


def find_galaxies(expanded: List[str]) -> List[Tuple[int, int]]:
    galaxies = []
    for y in range(0, len(expanded)):
        line = expanded[y]
        for x in range(0, len(line)):
            if line[x] == '#':
                galaxies.append((x, y))
    return galaxies


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)

    expanded = expand_universe(lines)
    galaxies = find_galaxies(expanded)

    return Input(data, lines, expanded, galaxies)


def parse_input_1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input_2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def calculate_distances(lines: List[str], galaxies: List[Tuple[int, int]], amount: int) -> int:
    distances = []
    for main_idx in range(0, len(galaxies)):
        for pair_idx in range(main_idx + 1, len(galaxies)):
            xa, ya = galaxies[main_idx]
            xb, yb = galaxies[pair_idx]

            xd = 0
            for x in range(min(xa, xb), max(xa, xb)):
                y = min(ya, yb)
                point = lines[y][x]
                xd += amount if point in ['E', '='] else 1

            yd = 0
            for y in range(min(ya, yb), max(ya, yb)):
                x = max(xa, xb)
                point = lines[y][x]
                yd += amount if point in ['E', '|'] else 1
            distances.append(xd + yd)
    return sum(distances)


@timer
def solve_1(input: Input) -> Optional[int]:
    return calculate_distances(input.expanded, input.galaxies, 2)


@timer
def solve_2(input: Input) -> Optional[int]:
    return calculate_distances(input.expanded, input.galaxies, 1000000)


# ==== Solutions with test data ==== #


test_data_1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
test_answer_1 = 374

test_data_2 = test_data_1
test_answer_2 = 82000210


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
