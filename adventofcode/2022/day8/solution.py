from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict
import numpy as np


# === Useful Functions === #


def splitlines(data: str, func=lambda x: x) -> List[str]:
    return [func(line) for line in data.splitlines() if line]


# ==== Types ==== #


@dataclass
class Input:
    width: int
    height: int
    grid: np.ndarray


# === Input parsing === #


def parse_input(data: str) -> Input:
    lines = splitlines(data)
    height = len(lines)
    width = len(lines[0])
    grid = np.zeros((width, height), dtype=int)
    for i, line in enumerate(lines):
        for j, value in enumerate(line):
            grid[i][j] = int(value)
    return Input(width, height, grid)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def is_tree_visible(input: Input, x: int, y: int) -> bool:
    grid = input.grid
    tree = grid[x][y]

    # Left
    seen = True
    for i in range(0, x):
        if grid[i][y] >= tree:
            seen = False
            break
    if seen:
        return True

    # Right
    seen = True
    for i in range(x+1, input.width):
        if grid[i][y] >= tree:
            seen = False
            break
    if seen:
        return True

    # Up
    seen = True
    for j in range(0, y):
        if grid[x][j] >= tree:
            seen = False
            break
    if seen:
        return True

    # Down
    seen = True
    for j in range(y+1, input.height):
        if grid[x][j] >= tree:
            seen = False
            break
    if seen:
        return True

    return False


def tree_scenic_score(input: Input, x: int, y: int) -> int:
    grid = input.grid
    tree = grid[x][y]

    # Left
    left = 0
    for i in range(x - 1, -1, -1):
        left += 1
        if grid[i][y] >= tree:
            break

    # Right
    right = 0
    for i in range(x+1, input.width):
        right += 1
        if grid[i][y] >= tree:
            break

    # Up
    up = 0
    for j in range(y - 1, -1, -1):
        up += 1
        if grid[x][j] >= tree:
            break

    # Down
    down = 0
    for j in range(y+1, input.height):
        down += 1
        if grid[x][j] >= tree:
            break

    return left * right * up * down


def solve1(input: Input) -> Optional[int]:
    edge_trees = 2 * (input.width + input.height) - 4
    inner_trees = 0
    # Go through inner trees
    for x in range(1, input.width - 1):
        for y in range(1, input.height - 1):
            if is_tree_visible(input, x, y):
                inner_trees += 1
    return edge_trees + inner_trees


def solve2(input: Input) -> Optional[int]:
    scores = []
    for x in range(1, input.width - 1):
        for y in range(1, input.height - 1):
            score = tree_scenic_score(input, x, y)
            scores.append(score)
    return max(scores)


# ==== Solutions with test data ==== #


test_data1 = """30373
25512
65332
33549
35390
"""
test_answer1 = 21

test_data2 = test_data1
test_answer2 = 8

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
                    f'Solution {number} - Test has failed. Should be {answer}, got {slv}')
                number += 1
                continue

            slv = func(parse(input))
            if slv is not None:
                print(f'Solution {number} - The answer: {slv}')
            number += 1
