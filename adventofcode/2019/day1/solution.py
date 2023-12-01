from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from functools import cache


# === Useful Functions === #


def splitlines(data: str, fun=lambda x: x) -> List[str]:
    return [fun(line) for line in data.splitlines() if line]


# === Types === #


@dataclass
class Input:
    masses: List[int]


# === Input parsing === #


def parse_input(data: str, options: dict) -> Input:
    masses = []
    for line in splitlines(data):
        masses.append(int(line))
    return Input(masses)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


@cache
def fuel_for_mass(mass: int) -> int:
    if mass <= 0:
        return 0
    fuel = max(int(mass // 3 - 2), 0)
    return fuel + fuel_for_mass(fuel)


def solve1(input: Input) -> Optional[int]:
    total_fuel = 0
    for mass in input.masses:
        total_fuel += int(mass // 3 - 2)
    return total_fuel


def solve2(input: Input) -> Optional[int]:
    total_fuel = 0
    for mass in input.masses:
        total_fuel += fuel_for_mass(mass)
    return total_fuel


# ==== Solutions with test data ==== #


test_data1 = """12
14
1969
100756"""
test_answer1 = 34241

test_data2 = """14
1969
100756"""
test_answer2 = 51314

solves = [
    {'func': solve1, 'parse': parse_input1,
        'test_data': test_data1, 'test_answer': test_answer1},
    {'func': solve2, 'parse': parse_input2,
        'test_data': test_data2, 'test_answer': test_answer2},
]

# ==== Template for running solutions ==== #


if __name__ == '__main__':
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
