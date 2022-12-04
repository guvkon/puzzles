#!/usr/bin/env python3

from enum import Enum
from typing import List, Optional, Tuple, Union


# ==== Solutions ==== #


def get_pairs(data: str) -> List[Tuple[Tuple[int, int]]]:
    pairs = []
    for line in data.splitlines():
        if not line:
            continue
        chunks = line.split(',')
        pair = []
        for chunk in chunks:
            chunk = chunk.split('-')
            pair.append((int(chunk[0]), int(chunk[1])))
        pairs.append(tuple(pair))
    return pairs


def is_pair_vore(pair: Tuple[Tuple[int, int]]) -> bool:
    left = pair[0]
    right = pair[1]
    if left[0] >= right[0] and left[1] <= right[1]:
        return True
    if right[0] >= left[0] and right[1] <= left[1]:
        return True
    return False


def is_pair_partially_vore(pair: Tuple[Tuple[int, int]]) -> bool:
    left = pair[0]
    right = pair[1]
    left_set = set([point for point in range(left[0], left[1] + 1)])
    right_set = set([point for point in range(right[0], right[1] + 1)])
    return len(left_set.intersection(right_set))


def is_point_inside(point: int, pair: Tuple[int, int]) -> bool:
    return pair[0] <= point <= pair[1]


def solve1(data: str) -> Optional[int]:
    score = 0
    for pair in get_pairs(data):
        if is_pair_vore(pair):
            score += 1
    return score


def solve2(data: str) -> Optional[int]:
    score = 0
    for pair in get_pairs(data):
        if is_pair_partially_vore(pair):
            score += 1
    return score


# ==== Solutions with test data ==== #


test_data1 = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
test_answer1 = 2

test_data2 = test_data1
test_answer2 = 4

solves = [
    {'func': solve1, 'test_data': test_data1, 'test_answer': test_answer1},
    {'func': solve2, 'test_data': test_data2, 'test_answer': test_answer2},
]

# ==== Template for running solutions ==== #


if __name__ == '__main__':
    filename = 'input.txt'
    with open(filename, 'r') as f:
        input = f.read()

        number = 1
        for solve in solves:
            func = solve['func']

            slv = func(solve['test_data'])
            answer = solve['test_answer']
            if slv == answer:
                print(f'Solution {number} - Test has passed')
            else:
                print(
                    f'Solution {number} - Test has failed. Should be {answer}, got {slv}')
                number += 1
                continue

            slv = func(input)
            if slv is not None:
                print(f'Solution {number} - The answer: {slv}')
            number += 1
