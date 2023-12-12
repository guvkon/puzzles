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


class Condition(Enum):
    operational = '.'
    damaged = '#'
    unknown = '?'


@dataclass
class Row:
    springs: str
    damaged: List[int]


@dataclass
class Input:
    data: str
    lines: List[str]
    rows: List[Row]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    rows = []
    for line in lines:
        parts = line.split(' ')
        damaged = [int(d) for d in parts[1].split(',')]
        rows.append(Row(parts[0], damaged))
    return Input(data, lines, rows)


def parse_input_1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input_2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def count_arrangements(row: Row) -> int:
    regex = []
    for d in row.damaged:
        regex.append(r'([\?#]{3})')
    return 0


@timer
def solve_1(input: Input) -> Optional[int]:
    sum = 0
    for row in input.rows:
        print(row)
        sum += count_arrangements(row)
    return


@timer
def solve_2(input: Input) -> Optional[int]:
    return


# ==== Solutions with test data ==== #


test_data_1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
test_answer_1 = 21

test_data_2 = test_data_1
test_answer_2 = 0


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
