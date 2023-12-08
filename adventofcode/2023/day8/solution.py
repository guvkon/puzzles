from __future__ import annotations

import numpy as np
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
class A:
    pass


@dataclass
class Input:
    lines: List[str]
    instructions: str
    map: Dict[str, Tuple[str, str]]
    starting_locations: List[str]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    map = {}
    starting_locations = []
    for idx in range(1, len(lines)):
        line = lines[idx]
        result = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
        map[result[1]] = (result[2], result[3])
        if result[1][2] == 'A':
            starting_locations.append(result[1])

    return Input(lines, lines[0], map, starting_locations)


def parse_input_1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input_2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


instruction_map = {'L': 0, 'R': 1}


@timer
def solve_1(input: Input) -> Optional[int]:
    idx = 0
    location = 'AAA'
    map = input.map
    steps = 0
    while location != 'ZZZ':
        instruction = instruction_map[input.instructions[idx]]
        location = map[location][instruction]
        idx += 1
        steps += 1
        if idx == len(input.instructions):
            idx = 0
    return steps


def is_end(locations: List[str]) -> bool:
    for loc in locations:
        if loc[2] != 'Z':
            return False
    return True


@timer
def solve_2(input: Input) -> Optional[int]:
    idx = 0
    steps = 0
    map = input.map
    instructs = input.instructions
    locations = input.starting_locations
    while not is_end(locations):
        instruction = instruction_map[instructs[idx]]
        for i, loc in enumerate(locations):
            locations[i] = map[loc][instruction]
        idx += 1
        steps += 1
        if idx == len(instructs):
            idx = 0
        if steps % 1e6 == 0:
            print(f'Steps = {steps}')
            print(locations)
    return steps


# ==== Solutions with test data ==== #


test_data_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
test_answer_1 = 2

test_data_2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
test_answer_2 = 6


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
