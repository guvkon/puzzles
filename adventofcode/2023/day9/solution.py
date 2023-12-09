from __future__ import annotations

import numpy
import math
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from time import time_ns
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
    lines: List[str]
    values: List[List[int]]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    values = [[int(v) for v in line.split(' ')] for line in lines]
    return Input(lines, values)


def parse_input_1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input_2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


memoize = {}


def next_value(seq: List[int]) -> int:
    key = ' '.join([str(s) for s in seq])
    if key in memoize:
        return memoize[key]

    all_zeroes = True
    for val in seq:
        if val != 0:
            all_zeroes = False
            break
    if all_zeroes:
        memoize[key] = 0
        return 0

    diffs = []
    last_idx = len(seq) - 1
    for idx in range(0, last_idx):
        diffs.append(seq[idx + 1] - seq[idx])
    answer = seq[last_idx] + next_value(diffs)
    memoize[key] = answer
    return answer


@timer
def solve_1(input: Input) -> Optional[int]:
    values = input.values
    sum = 0
    for seq in values:
        sum += next_value(seq)
    return sum


@timer
def solve_2(input: Input) -> Optional[int]:
    values = input.values
    sum = 0
    for seq in values:
        seq.reverse()
        sum += next_value(seq)
    return sum


# ==== Solutions with test data ==== #


test_data_1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
test_answer_1 = 114

test_data_2 = test_data_1
test_answer_2 = 2


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
