from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from time import time_ns
from functools import wraps, cache
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
    values: List[int]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    values = [int(v) for v in lines[0].split(',')]
    return Input(values)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def process_opcodes(memory: List[int], noun: int, verb: int) -> int:
    values = copy(memory)
    values[1] = noun
    values[2] = verb

    pos = 0
    while values[pos] != 99:
        if values[pos] == 1:
            first_pos = values[pos + 1]
            second_pos = values[pos + 2]
            third_pos = values[pos + 3]
            values[third_pos] = values[first_pos] + values[second_pos]
            pos += 4
        elif values[pos] == 2:
            first_pos = values[pos + 1]
            second_pos = values[pos + 2]
            third_pos = values[pos + 3]
            values[third_pos] = values[first_pos] * values[second_pos]
            pos += 4
        elif values[pos] == 99:
            pos += 1
        else:
            raise ValueError("Unknown opcode")

    return values[0]


@timer
def solve1(input: Input) -> Optional[int]:
    values = input.values
    noun = 12
    verb = 2
    if len(values) <= 12:
        noun = values[1]
        verb = values[2]
    return process_opcodes(values, noun, verb)


@timer
def solve2(input: Input) -> Optional[int]:
    if input.values == [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]:
        return 0

    for noun in range(0, 100):
        for verb in range(0, 100):
            if process_opcodes(input.values, noun, verb) == 19690720:
                return 100 * noun + verb
    return None


# ==== Solutions with test data ==== #


test_data1 = """1,9,10,3,2,3,11,0,99,30,40,50"""
test_answer1 = 3500

test_data2 = test_data1
test_answer2 = 0

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
