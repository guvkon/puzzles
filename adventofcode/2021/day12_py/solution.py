#!/usr/bin/env python3

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Set, Dict, Generator
import numpy as np

# === Useful Functions === #


def splitlines(data: str, func) -> List[str]:
    return [func(line) for line in data.splitlines() if line]


# ==== Types ==== #


@dataclass
class Input:
    vertices: Set[str]
    edges: Set[Tuple[str, str]]
    graph: Dict[str, Set[str]]


# === Input parsing === #


def parse_input(data: str) -> Input:
    vertices = set()
    edges = set()
    graph: Dict[str, Set[str]] = {}
    for edge in splitlines(data, lambda x: x.split('-')):
        edges.add(tuple(edge))
        vertices.add(edge[0])
        vertices.add(edge[1])
    for vertix in vertices:
        graph[vertix] = set()
    for edge in edges:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])
    return Input(vertices, edges, graph)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def is_small_cave(cave: str) -> bool:
    return cave.lower() == cave


def paths1(input: Input, position: str, context: List[str]) -> List[List[str]]:
    paths = []
    graph = input.graph
    for next in graph[position]:
        if is_small_cave(next) and next in context:
            continue
        paths.append(context + [next])
    return paths


def find_finished_paths1(input: Input, position: str, context: List[str]) -> Generator[List[str], None, None]:
    for path in paths1(input, position, context):
        if is_path_finished(path):
            yield path
        elif path == context:
            continue  # Dead end.
        else:
            yield from find_finished_paths1(input, path[len(path) - 1], path)


def is_path_finished(path: List[str]) -> bool:
    return path[len(path) - 1] == 'end'


def small_cave_limit_reached(path: List[str]):
    small_caves = [cave for cave in path if is_small_cave(cave)]
    return len(small_caves) > len(list(set(small_caves)))


def paths2(input: Input, position: str, context: List[str]) -> List[List[str]]:
    paths = []
    graph = input.graph
    for next in graph[position]:
        if next == 'start':
            continue
        if is_small_cave(next) and small_cave_limit_reached(context) and next in context:
            continue
        paths.append(context + [next])
    return paths


def find_finished_paths2(input: Input, position: str, context: List[str]) -> Generator[List[str], None, None]:
    for path in paths2(input, position, context):
        if is_path_finished(path):
            yield path
        elif path == context:
            continue  # Dead end.
        else:
            yield from find_finished_paths2(input, path[len(path) - 1], path)


def solve1(input: Input) -> Optional[int]:
    finished_paths = []
    for path in find_finished_paths1(input, 'start', ['start']):
        finished_paths.append(path)
    return len(finished_paths)


def solve2(input: Input) -> Optional[int]:
    finished_paths = []
    for path in find_finished_paths2(input, 'start', ['start']):
        finished_paths.append(path)
    return len(finished_paths)


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
test_answer2 = 36

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
