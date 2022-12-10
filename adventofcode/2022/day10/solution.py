from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set
import numpy as np


# === Useful Functions === #


def splitlines(data: str, func=lambda x: x) -> List[str]:
    return [func(line) for line in data.splitlines() if line]


# 20th, 60th, 100th, 140th, 180th, and 220th


@dataclass
class Operation:
    cycles: int
    register: int


@dataclass
class Input:
    operations: List[Operation]


# === Input parsing === #


def parse_input(data: str) -> Input:
    operations = []
    for line in splitlines(data, lambda x: x.split(' ')):
        match line[0]:
            case 'addx':
                operations.append(Operation(2, int(line[1])))
            case 'noop':
                operations.append(Operation(1, 0))
    return Input(operations)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def get_cycles(input: Input) -> List[int]:
    cycles = [1]
    register = 1
    for op in input.operations:
        for _ in range(0, op.cycles):
            cycles.append(register)
        register += op.register
    return cycles


def solve1(input: Input) -> Optional[int]:
    cycles_of_note = [20, 60, 100, 140, 180, 220]
    cycles = get_cycles(input)
    score = 0
    for cycle in cycles_of_note:
        val = cycles[cycle]
        score += val * cycle
    return score


def draw(screen: np.ndarray):
    output = ''
    for y in range(0, 6):
        for x in range(0, 40):
            output += screen[y][x]
        output += '\n'
    return output


def solve2(input: Input) -> Optional[str]:
    cycles = get_cycles(input)
    screen = np.zeros((6, 40), dtype=str)
    for cycle, register in enumerate(cycles):
        if cycle == 0:
            continue
        pixel_pos = cycle - 1
        y = pixel_pos // 40
        x = pixel_pos % 40
        pixel = [register - 1, register, register + 1]
        screen[y][x] = '#' if x in pixel else '.'
    return draw(screen)


# ==== Solutions with test data ==== #


test_data1 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
test_answer1 = 13140

test_data2 = test_data1
test_answer2 = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""

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
