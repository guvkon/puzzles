from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable


# === Useful Functions === #


def splitlines(data: str, fun=lambda x: x) -> List[str]:
    return [fun(line) for line in data.splitlines() if line]


# === Types === #


class Color(Enum):
    blue = 'blue'
    red = 'red'
    green = 'green'


@dataclass
class ColoredBalls:
    number: int
    color: Color


@dataclass
class BallSet:
    balls: List[ColoredBalls]


@dataclass
class Game:
    id: int
    sets: List[BallSet]
    line: str


@dataclass
class Input:
    lines: List[str]
    games: List[Game]


# === Input parsing === #


def parse_sets(line: str) -> List[BallSet]:
    sets = []
    for part in line.split(';'):
        colored_balls = []
        for ball_group in part.strip().split(','):
            info = ball_group.strip().split(' ')
            colored_balls.append(ColoredBalls(int(info[0]), Color(info[1])))
        sets.append(BallSet(colored_balls))
    return sets


def parse_line(line: str) -> Game:
    regex = r"Game (\d+): (.+)"
    result = re.match(regex, line)
    return Game(int(result[1]), parse_sets(result[2]), line)


def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    games = [parse_line(line) for line in lines]
    return Input(lines, games)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def is_game_possible(game: Game) -> bool:
    limits = {
        Color.red: 12,
        Color.green: 13,
        Color.blue: 14,
    }
    for set in game.sets:
        for ball in set.balls:
            if limits[ball.color] < ball.number:
                return False
    return True


def solve1(input: Input) -> Optional[int]:
    sum = 0
    for game in input.games:
        if is_game_possible(game):
            sum += game.id
    return sum


def game_power(game: Game) -> int:
    floors = {
        Color.red: 0,
        Color.green: 0,
        Color.blue: 0,
    }
    for set in game.sets:
        for ball in set.balls:
            if floors[ball.color] < ball.number:
                floors[ball.color] = ball.number
    return floors[Color.red] * floors[Color.green] * floors[Color.blue]


def solve2(input: Input) -> Optional[int]:
    total_power = 0
    for game in input.games:
        total_power += game_power(game)
    return total_power


# ==== Solutions with test data ==== #


test_data1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
test_answer1 = 8

test_data2 = test_data1
test_answer2 = 2286

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
