from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set
import numpy as np


# === Useful Functions === #


def splitlines(data: str, func=lambda x: x) -> List[str]:
    return [func(line) for line in data.splitlines() if line]


# ==== Types ==== #


@dataclass
class Position:
    x: int
    y: int


class Direction(Enum):
    Up = 'U'
    Down = 'D'
    Left = 'L'
    Right = 'R'


@dataclass
class Move:
    direction: Direction
    amount: int


@dataclass
class Input:
    moves: List[Move]


# === Input parsing === #


def parse_input(data: str) -> Input:
    moves = []
    for line in splitlines(data, lambda x: x.split(' ')):
        if line[0] == 'U':
            direction = Direction.Up
        elif line[0] == 'D':
            direction = Direction.Down
        elif line[0] == 'L':
            direction = Direction.Left
        else:
            direction = Direction.Right
        moves.append(Move(direction, int(line[1])))
    return Input(moves)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def is_touching(head: Position, tail: Position) -> bool:
    return abs(head.x - tail.x) <= 1 and abs(head.y - tail.y) <= 1


def solve1(input: Input) -> Optional[int]:
    head = Position(0, 0)
    tail = Position(0, 0)
    tail_visits = {(tail.x, tail.y)}
    for move in input.moves:
        direction = move.direction
        for _ in range(0, move.amount):
            match direction:
                case Direction.Up:
                    head.y += 1
                case Direction.Down:
                    head.y -= 1
                case Direction.Right:
                    head.x += 1
                case Direction.Left:
                    head.x -= 1
            if not is_touching(head, tail):
                if head.x == tail.x:
                    tail.y += int((head.y - tail.y) / abs(head.y - tail.y))
                elif head.y == tail.y:
                    tail.x += int((head.x - tail.x) / abs(head.x - tail.x))
                else:
                    tail.x += int((head.x - tail.x) / abs(head.x - tail.x))
                    tail.y += int((head.y - tail.y) / abs(head.y - tail.y))
                tail_visits.add((tail.x, tail.y))
    return len(tail_visits)


def solve2(input: Input) -> Optional[int]:
    head = Position(0, 0)
    tails: List[Position] = []
    for _ in range(0, 9):
        tails.append(Position(0, 0))
    tail_visits = {(tails[8].x, tails[8].y)}
    for move in input.moves:
        direction = move.direction
        for _ in range(0, move.amount):
            match direction:
                case Direction.Up:
                    head.y += 1
                case Direction.Down:
                    head.y -= 1
                case Direction.Right:
                    head.x += 1
                case Direction.Left:
                    head.x -= 1
            for index, tail in enumerate(tails):
                _head = head if index == 0 else tails[index - 1]
                if not is_touching(_head, tail):
                    if _head.x == tail.x:
                        tail.y += int((_head.y - tail.y) / abs(_head.y - tail.y))
                    elif _head.y == tail.y:
                        tail.x += int((_head.x - tail.x) / abs(_head.x - tail.x))
                    else:
                        tail.x += int((_head.x - tail.x) / abs(_head.x - tail.x))
                        tail.y += int((_head.y - tail.y) / abs(_head.y - tail.y))
            tail_visits.add((tails[8].x, tails[8].y))
    return len(tail_visits)


# ==== Solutions with test data ==== #


test_data1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
test_answer1 = 13

test_data2 = test_data1
test_answer2 = 1

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
