#!/usr/bin/env python3

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Set, Dict
import numpy as np

# === Useful Functions === #


def splitlines(data: str, func) -> List[str]:
    return [func(line) for line in data.splitlines() if not line]


# ==== Types ==== #


@dataclass
class Input:
    vertices: Set
    edges: Set[Tuple[str, str]]
    graph: Dict[str, Dict[str, bool]]


# === Input parsing === #


def parse_input(data: str) -> Input:
    vertices = set()
    edges = set()
    graph = {}
    for edge in splitlines(data, lambda x: x.split('-')):
        edges.add(tuple(edge))
        vertices.add(edge[0])
        vertices.add(edge[1])
    for vertix in vertices:
        matrix = {}
        for vertix2 in vertices:
            matrix[vertix2] = False
        graph[vertix] = matrix
    for edge in edges:
        graph[edge[0]][edge[1]] = True
        graph[edge[1]][edge[0]] = True
    return Input(vertices, edges, graph)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def is_big_cave(cave: str) -> bool:
    return cave.upper() == cave


def is_small_cave(cave: str) -> bool:
    return not is_big_cave


def solve1(input: Input) -> Optional[int]:
    return None


def solve2(input: Input) -> Optional[int]:
    return None


# ==== Solutions with test data ==== #


test_data1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
test_answer1 = 10

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
