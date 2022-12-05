#!/usr/bin/env python3

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union


# ==== Types ==== #


@dataclass
class Move:
    amount: int
    start: int
    end: int


@dataclass
class Input:
    moves: List[Move]
    stacks: List[List[str]]


# === Input parsing === #


def parse_input(data: str) -> Input:
    hstacks = []
    moves = []
    building_stacks = True
    for index, line in enumerate(data.splitlines()):
        if not line:
            continue
        if building_stacks:
            if '1' in line:
                building_stacks = False
                continue
            stack = []
            stacks_count = len(line) // 4 + 1
            for index in range(0, stacks_count):
                stack.append(line[index*(stacks_count+1)+1:index*(stacks_count+1)+2])
            hstacks.append(stack)
        else:
            # move 12 from 9 to 3
            matches = re.search('move (\d+) from (\d+) to (\d+)', line)
            moves.append(Move(
                int(matches[1]), int(matches[2]), int(matches[3])))  # type: ignore
    vstacks = []
    stacks_width = len(hstacks[0])
    stacks_height = len(hstacks)
    for w_index in range(0, stacks_width):
        stack = []
        for h_index in range(stacks_height - 1, -1, -1):
            crate = hstacks[h_index][w_index]
            if crate != ' ':
                stack.append(hstacks[h_index][w_index])
        vstacks.append(stack)
    return Input(moves, vstacks)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def solve1(input: Input) -> Optional[str]:
    print(input)
    return None


def solve2(input: Input) -> Optional[str]:
    return None


# ==== Solutions with test data ==== #


test_data1 = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
test_answer1 = 'CMZ'

test_data2 = test_data1
test_answer2 = 'CMZ'

solves = [
    {'func': solve1, 'parse': parse_input1, 'test_data': test_data1, 'test_answer': test_answer1},
    # {'func': solve2, 'parse': parse_input2, 'test_data': test_data2, 'test_answer': test_answer2},
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
