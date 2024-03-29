from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from time import time_ns
from functools import wraps, cache, cached_property
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
    times: List[int]
    distances: List[int]
    time: int
    distance: int


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)

    result = re.match(r'Time: +(.+)', lines[0])
    times = [int(t) for t in result[1].split(' ') if t]

    result = re.match(r'Distance: +(.+)', lines[1])
    distances = [int(t) for t in result[1].split(' ') if t]

    time = int(lines[0].replace('Time:', '').replace(' ', ''))
    distance = int(lines[1].replace('Distance:', '').replace(' ', ''))

    return Input(lines, times, distances, time, distance)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def find_winners(time: int, dist: int) -> List[Tuple[int, int]]:
    winners = []
    for t in range(0, time + 1):
        remaining_t = time - t
        d = remaining_t * t
        if d > dist:
            winners.append((t, d))
    return winners


@timer
def solve1(input: Input) -> Optional[int]:
    answer = 1
    for idx in range(0, len(input.times)):
        time = input.times[idx]
        dist = input.distances[idx]
        winners = find_winners(time, dist)
        answer *= len(winners)
    return answer


@timer
def solve2(input: Input) -> Optional[int]:
    winners = find_winners(input.time, input.distance)
    return len(winners)


# ==== Solutions with test data ==== #


test_data1 = """Time:      7  15   30
Distance:  9  40  200"""
test_answer1 = 288

test_data2 = test_data1
test_answer2 = 71503

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
