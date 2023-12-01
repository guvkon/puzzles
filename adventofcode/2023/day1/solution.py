from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable


# === Useful Functions === #


def splitlines(data: str, fun=lambda x: x) -> List[str]:
    return [fun(line) for line in data.splitlines() if line]


# === Types === #


@dataclass
class Input:
    lines: List[str]


# === Input parsing === #


def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    return Input(lines)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def solve1(input: Input) -> Optional[int]:
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    sum = 0
    for line in input.lines:
        number = ''
        for char in line:
            if char in numbers:
                number += char
                break
        for char in reversed(line):
            if char in numbers:
                number += char
                break
        sum += int(number)
    return sum


def text_to_number(text: str) -> str:
    if text == 'one':
        return '1'
    elif text == 'two':
        return '2'
    elif text == 'three':
        return '3'
    elif text == 'four':
        return '4'
    elif text == 'five':
        return '5'
    elif text == 'six':
        return '6'
    elif text == 'seven':
        return '7'
    elif text == 'eight':
        return '8'
    elif text == 'nine':
        return '9'
    else:
        return text


def solve2(input: Input) -> Optional[int]:
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    sum = 0
    for line in input.lines:
        print(line)
        number = ''

        left_index = len(line) - 1
        left_number = ''
        for num in numbers:
            index = line.find(num)
            if -1 < index <= left_index:
                left_index = index
                left_number = num
                print(f'left {index} - {num}')

        number += text_to_number(left_number)

        right_index = 0
        right_number = ''
        for num in numbers:
            index = line.rfind(num)
            if index > -1 and index >= right_index:
                right_index = index
                right_number = num
                print(f'right {index} - {num}')
        number += text_to_number(right_number)
        print(f'number {number}')

        sum += int(number)

    return sum


# ==== Solutions with test data ==== #


test_data1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
test_answer1 = 142

test_data2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
test_answer2 = 281

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
