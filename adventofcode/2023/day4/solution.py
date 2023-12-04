from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from time import time_ns
from functools import wraps, cache


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
class Card:
    id: int
    winning_numbers: List[int]
    numbers_got: List[int]
    line: str


@dataclass
class Input:
    lines: List[str]
    cards: List[Card]


# === Input parsing === #


def parse_line(line: str) -> Card:
    regex = r"Card +(\d+): (.+) \| (.+)"
    result = re.match(regex, line)
    return Card(
        int(result[1]),
        [int(n.strip()) for n in re.sub(r' +', ' ', result[2].strip()).split(' ')],
        [int(n.strip()) for n in re.sub(r' +', ' ', result[3].strip()).split(' ')],
        line
    )


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    cards = [parse_line(line) for line in lines]
    return Input(lines, cards)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def count_winners(card: Card) -> int:
    winners = 0
    for num in card.winning_numbers:
        if num in card.numbers_got:
            winners += 1
    return winners


@timer
def solve1(input: Input) -> Optional[int]:
    sum = 0
    for card in input.cards:
        winners = count_winners(card)
        if winners:
            sum += pow(2, winners - 1)
    return sum


@timer
def solve2(input: Input) -> Optional[int]:
    sum = 0
    extra_cards = {}
    for card in input.cards:
        extra = extra_cards.get(card.id, 0)
        winners = count_winners(card)
        if winners:
            for idx in range(card.id + 1, card.id + 1 + winners):
                extra_cards[idx] = extra_cards.get(idx, 0) + 1 + extra
        sum += 1 + extra
    return sum


# ==== Solutions with test data ==== #


test_data1 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
test_answer1 = 13

test_data2 = test_data1
test_answer2 = 30

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
