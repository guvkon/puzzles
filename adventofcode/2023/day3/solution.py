from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from functools import wraps
from time import time_ns


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


DIGITS = '1234567890'


# === Types === #


@dataclass
class Input:
    lines: List[str]
    width: int
    height: int


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    width = len(lines[0])
    height = len(lines)

    return Input(lines, width, height)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def solve1(input: Input) -> Optional[int]:
    width = input.width
    height = input.height
    matrix = input.lines

    def has_adjacent_symbol(start_x, x, y, verbose: bool = False) -> bool:
        if verbose:
            print('verbose')
            print(start_x, x, y)
        for _y in range(max(0, y - 1), min(y + 2, height)):
            for _x in range(max(0, start_x - 1), min(x + 1, width)):
                _val = matrix[_y][_x]
                if _val not in DIGITS and _val != '.':
                    return True
        return False

    part_numbers = []
    y = 0
    while y < height:
        x = 0
        start_x = x
        digit = ''
        x_part_numbers = []
        while x < width:
            val = matrix[y][x]
            if val in DIGITS:
                if digit == '':
                    start_x = x
                digit += val
            if val not in DIGITS or x == width - 1:
                # Number has ended.
                if digit:
                    if has_adjacent_symbol(start_x, x, y):
                        part_numbers.append(int(digit))
                        x_part_numbers.append(int(digit))
                    digit = ''
            x += 1
        print('%5d : %s' % (y, x_part_numbers))
        y += 1

    return sum(part_numbers)


def solve2(input: Input) -> Optional[int]:
    return None


# ==== Solutions with test data ==== #


test_data1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
test_answer1 = 4361

test_data2 = test_data1
test_answer2 = 467835

solves = [
    {'func': solve1, 'parse': parse_input1,
     'test_data': test_data1, 'test_answer': test_answer1},
    {'func': solve2, 'parse': parse_input2,
     'test_data': test_data2, 'test_answer': test_answer2},
]

# ==== Template for running solutions ==== #


@timer
def main():
    filename = 'input.txt'
    with open(filename, 'r') as f:
        input = f.read()

        number = 1
        for solve in solves:
            func = solve['func']
            parse = solve['parse']

            slv = func(parse(solve['test_data']))
            answer = solve['test_answer']
            if slv == answer:
                print(f'Solution {number} - Test has passed')
            else:
                print(
                    f'Solution {number} - Test has failed. Should be:\n{answer}\nGot:\n{slv}')
                number += 1
                continue

            slv = func(parse(input))
            if slv is not None:
                print(f'Solution {number} - The answer:\n{slv}')
            number += 1


if __name__ == '__main__':
    main()
