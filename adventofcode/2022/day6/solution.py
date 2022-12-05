#!/usr/bin/env python3

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union


# === Useful Functions === #


def splitlines(data: str) -> List[str]:
    return [line for line in data.splitlines() if not line]


# ==== Types ==== #


@dataclass
class Input:
    items: list


# === Input parsing === #


def parse_input(data: str) -> Input:
    return Input(splitlines(data))


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def solve1(input: Input) -> Optional[str]:
    return None


def solve2(input: Input) -> Optional[str]:
    return None


# ==== Solutions with test data ==== #


test_data1 = """
"""
test_answer1 = 0

test_data2 = test_data1
test_answer2 = 0

solves = [
    {'func': solve1, 'parse': parse_input1, 'test_data': test_data1, 'test_answer': test_answer1},
    {'func': solve2, 'parse': parse_input2, 'test_data': test_data2, 'test_answer': test_answer2},
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
                    f'Solution {number} - Test has failed. Should be {answer}, got {slv}')
                number += 1
                continue

            slv = func(parse(input))
            if slv is not None:
                print(f'Solution {number} - The answer: {slv}')
            number += 1
