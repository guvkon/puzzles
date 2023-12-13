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
class Pattern:
    left: str
    right: Optional[str]

    @property
    def wiggle(self) -> bool:
        return self.right is not None


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


def count_potential_permutations(springs: str) -> int:
    exp = 0
    for s in springs:
        if s == '?':
            exp += 1
    return pow(2, exp)


start_left = r'[\.\?]*?'
start_right = r'[\.\?]*'
between_left = r'[\.\?]+?'
between_right = r'[\.\?]+'
end = r'[\.\?]*$'


def damaged(length: int) -> str:
    return r'([#\?]{' + str(length) + r'})'


def between(length: int) -> str:
    return r'[\.\?]{' + str(length) + r'}'


def count_arrangements(row: Row) -> int:
    patterns = [Pattern(start_left, start_right)]
    # Example: r'^[\.\?]*?([#\?]{1})[\.\?]+?([#\?]{6})[\.\?]+([#\?]{5})[\.\?]*$'
    for count, d in enumerate(row.damaged):
        patterns.append(Pattern(damaged(d), None))
        if count < len(row.damaged) - 1:
            patterns.append(Pattern(between_left, between_right))
    patterns.append(Pattern(end, None))

    def patterns_step(left_regex: List[str], group: int) -> int:
        print(f'Left regex = {left_regex}')
        print(f'Group = {group}')
        if len(left_regex) == len(patterns):
            print('Patterns matched the length of left_regex')
            return 1

        if group > len(row.damaged):
            print('Group exceeded number of damaged')
            return 1

        index = len(left_regex)
        pattern = patterns[index]
        if not pattern.wiggle:
            new_regex = [r for r in left_regex]
            new_regex.append(pattern.left)
            return patterns_step(new_regex, group + 1)

        before = ''.join(left_regex)
        remaining = ''.join([patterns[idx].left for idx in range(index + 1, len(patterns))])
        _left_regex = f'{before}({pattern.left}){remaining}'
        print(f'Actual regex = {_left_regex}')
        left_match = re.search(_left_regex, row.springs)
        if not left_match:
            return 0
        left = left_match.start(group + 1)
        vary_start = len(left_match.group(group))
        _right_regex = before + pattern.right + remaining
        right_match = re.search(_right_regex, row.springs)
        right = right_match.start(group)
        print(f'Left = {left}, right = {right}, vary_start = {vary_start}')

        if left == right:
            new_regex = [r for r in left_regex]
            new_regex.append(pattern.left)
            return patterns_step(new_regex, group)

        count = 0
        for vary in range(vary_start, vary_start + right - left + 1):
            new_regex = [r for r in left_regex]
            new_regex.append(between(vary))
            count += patterns_step(new_regex, group)
        return count

    return patterns_step([], 1)


@timer
def solve_1(input: Input) -> Optional[int]:
    sum = 0
    print()
    for row in input.rows:
        print(row)
        arrangements = count_arrangements(row)
        print(f'Arrangements = {arrangements}\n')
        sum += arrangements
    print()
    return sum


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
