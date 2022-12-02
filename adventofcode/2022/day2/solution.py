#!/usr/bin/env python3

from enum import Enum
from typing import List, Optional, Tuple, Union


# ==== Solutions ==== #


"""
A, X - Rock
B, Y - Paper
C, Z - Scossors
X - 1
Y - 2
Z - 3
"""


class Outcome(Enum):
    WIN = 6
    DRAW = 3
    LOSS = 0


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def play_rps(opp: Shape, me: Shape) -> Outcome:
    if me == opp:
        return Outcome.DRAW
    if me == Shape.ROCK:
        if opp == Shape.PAPER:
            return Outcome.LOSS
        if opp == Shape.SCISSORS:
            return Outcome.WIN
    if me == Shape.PAPER:
        if opp == Shape.ROCK:
            return Outcome.WIN
        if opp == Shape.SCISSORS:
            return Outcome.LOSS
    if me == Shape.SCISSORS:
        if opp == Shape.ROCK:
            return Outcome.LOSS
        if opp == Shape.PAPER:
            return Outcome.WIN


def unplay_rps(opp: Shape, outcome: Outcome) -> Shape:
    if outcome == Outcome.DRAW:
        return opp
    if outcome == Outcome.WIN:
        if opp == Shape.ROCK:
            return Shape.PAPER
        if opp == Shape.PAPER:
            return Shape.SCISSORS
        if opp == Shape.SCISSORS:
            return Shape.ROCK
    if outcome == Outcome.LOSS:
        if opp == Shape.ROCK:
            return Shape.SCISSORS
        if opp == Shape.PAPER:
            return Shape.ROCK
        if opp == Shape.SCISSORS:
            return Shape.PAPER


def parse_shape(shape: str) -> Shape:
    if shape in ['A', 'X']:
        return Shape.ROCK
    if shape in ['B', 'Y']:
        return Shape.PAPER
    if shape in ['C', 'Z']:
        return Shape.SCISSORS
    raise ValueError('Shape must be only A, B, C, X, Y, Z!')


def parse_outcome(outcome: str) -> Outcome:
    if outcome == 'X':
        return Outcome.LOSS
    if outcome == 'Y':
        return Outcome.DRAW
    if outcome == 'Z':
        return Outcome.WIN
    raise ValueError('Outcome must be only X, Y, Z')


def parse(data: str, with_outcome = False) -> Union[List[Tuple[Shape, Shape]], List[Tuple[Shape, Outcome]]]:
    rounds = []
    for line in data.splitlines():
        if not line:
            continue
        shapes = line.split(' ')
        left = parse_shape(shapes[0])
        right = parse_shape(shapes[1]) if not with_outcome else parse_outcome(shapes[1])
        round = (left, right)
        rounds.append(round)
    return rounds


def solve1(data: str) -> Optional[int]:
    rounds = parse(data)
    total_score = 0
    for round in rounds:
        outcome_score = play_rps(round[0], round[1]).value
        shape_score = round[1].value
        round_score = outcome_score + shape_score
        total_score += round_score
    return total_score


def solve2(data: str) -> Optional[int]:
    rounds = parse(data, with_outcome=True)
    total_score = 0
    for round in rounds:
        outcome_score = round[1].value
        shape_score = unplay_rps(round[0], round[1]).value
        round_score = outcome_score + shape_score
        total_score += round_score
    return total_score


# ==== Solutions with test data ==== #


test_data1 = """A Y
B X
C Z"""
test_answer1 = 15

test_data2 = test_data1
test_answer2 = 12

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
