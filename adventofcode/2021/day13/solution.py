from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set
import numpy as np


# === Useful Functions === #


def splitlines(data: str, func=lambda x: x) -> List[str]:
    return [func(line) for line in data.splitlines() if line]


@dataclass
class Fold:
    direction: str
    position: int


@dataclass
class Input:
    paper: np.ndarray
    folds: List[Fold]


# === Input parsing === #


def parse_input(data: str) -> Input:
    folds = []
    dots = []
    width = 0
    height = 0
    for line in splitlines(data):
        if 'fold' in line:
            fold = line[11:].split('=')
            folds.append(Fold(fold[0], int(fold[1])))
        else:
            [x, y] = [int(dot) for dot in line.split(',')]
            dots.append((x, y))
            width = max(width, x)
            height = max(height, y)
    paper = np.zeros((height + 1, width + 1), dtype=int)
    for (x, y) in dots:
        paper[y][x] = 1
    return Input(paper, folds)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def make_fold(paper: np.ndarray, fold: Fold) -> np.ndarray:
    (height, width) = paper.shape
    if fold.direction == 'y':
        new_height = height // 2
        folded_paper = np.zeros((new_height, width))
        for y in range(0, new_height):
            for x in range(0, width):
                folded_paper[y][x] = paper[y][x] + paper[height - y - 1][x]
    else:
        new_width = width // 2
        folded_paper = np.zeros((height, new_width))
        for x in range(0, new_width):
            for y in range(0, height):
                folded_paper[y][x] = paper[y][x] + paper[y][width - x - 1]
    return folded_paper


def draw(paper: np.ndarray) -> str:
    output = ''
    (height, width) = paper.shape
    for y in range(0, height):
        for x in range(0, width):
            dot = paper[y][x]
            output += '#' if dot > 0 else ' '
        output += '\n'
    return output


def solve1(input: Input) -> Optional[int]:
    folded_paper = make_fold(input.paper, input.folds[0])
    score = 0
    for lines in folded_paper:
        for dot in lines:
            if dot > 0:
                score += 1
    return score


def solve2(input: Input) -> Optional[int]:
    paper = input.paper
    print(draw(paper))
    print('\n==================\n')
    for fold in input.folds:
        paper = make_fold(paper, fold)
        print(draw(paper))
        print('\n==================\n')
    return 0


# ==== Solutions with test data ==== #


test_data1 = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
test_answer1 = 17

test_data2 = test_data1
test_answer2 = 0

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
