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


class NodeType(Enum):
    top_bottom = '|'
    left_right = '-'
    top_right = 'L'
    top_left = 'J'
    bottom_left = '7'
    bottom_right = 'F'
    ground = '.'
    start = 'S'


class Node:
    type: NodeType
    x: int
    y: int

    def __init__(self, type: NodeType, x: int, y: int):
        self.type = type
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.type.value} ({self.x}, {self.y})'

    @property
    def pos(self) -> Tuple[int, int]:
        return self.x, self.y

    @property
    def top(self) -> bool:
        return self.type in [NodeType.top_left, NodeType.top_right, NodeType.top_bottom, NodeType.start]

    @property
    def bottom(self) -> bool:
        return self.type in [NodeType.bottom_right, NodeType.bottom_left, NodeType.top_bottom, NodeType.start]

    @property
    def left(self) -> bool:
        return self.type in [NodeType.left_right, NodeType.bottom_left, NodeType.top_left, NodeType.start]

    @property
    def right(self) -> bool:
        return self.type in [NodeType.left_right, NodeType.bottom_right, NodeType.top_right, NodeType.start]

    @property
    def is_start(self):
        return self.type == NodeType.start


@dataclass
class Input:
    data: str
    lines: List[str]
    nodes: Dict[Tuple[int, int], Node]
    start: Node
    edges: Dict[Tuple[int, int], List[Node]]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)

    nodes = {}
    edges = {}
    start = None
    # Build nodes, init edges, and find start.
    for x in range(0, len(lines[0])):
        for y in range(len(lines)):
            node = Node(NodeType(lines[y][x]), x, y)
            nodes[node.pos] = node
            edges[node.pos] = []
            if node.is_start:
                start = node
    # Build edges.
    for node in nodes.values():
        x, y = node.pos
        if node.right:
            right = nodes.get((x + 1, y))
            if right and right.left:
                edges[node.pos].append(right)
                edges[right.pos].append(node)
        if node.bottom:
            bottom = nodes.get((x, y + 1))
            if bottom and bottom.top:
                edges[node.pos].append(bottom)
                edges[bottom.pos].append(node)
    if not start:
        raise ValueError('Cannot find start node')
    return Input(data, lines, nodes, start, edges)


def parse_input_1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input_2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def generate_starting_loops(start: Node, connected_nodes: List[Node]) -> List[List[Node]]:
    edges = {}
    for node in connected_nodes:
        edges[node.pos] = node
    x, y = start.pos
    left = edges.get((x - 1, y))
    right = edges.get((x + 1, y))
    top = edges.get((x, y - 1))
    bottom = edges.get((x, y + 1))
    if top and bottom:
        yield [Node(NodeType.top_bottom, x, y), top]
    if top and left:
        yield [Node(NodeType.top_left, x, y), top]
    if top and bottom:
        yield [Node(NodeType.top_bottom, x, y), top]
    if left and bottom:
        yield [Node(NodeType.bottom_left, x, y), bottom]
    if left and right:
        yield [Node(NodeType.left_right, x, y), right]
    if bottom and right:
        yield [Node(NodeType.bottom_right, x, y), right]


@timer
def solve_1(input: Input) -> Optional[int]:
    start = input.start
    edges = input.edges
    max_loop = 0
    for loop in generate_starting_loops(start, edges[start.pos]):
        finished = False
        while True:
            curr = len(loop) - 1
            curr_node = loop[curr]
            prev_node = loop[curr - 1]
            if len(edges[curr_node.pos]) != 2:
                break
            for node in edges[curr_node.pos]:
                if node.pos != prev_node.pos:
                    loop.append(node)
            if loop[len(loop) - 1].pos == start.pos:
                finished = True
                loop.pop()
                break

        if not finished:
            continue
        if max_loop < len(loop):
            max_loop = len(loop)

    return max_loop // 2


@timer
def solve_2(input: Input) -> Optional[int]:
    return


# ==== Solutions with test data ==== #


test_data_1 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
test_answer_1 = 8

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
