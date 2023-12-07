from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from time import time_ns
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


class HandType(Enum):
    five_of_a_kind = 7
    four_of_a_kind = 6
    full_house = 5
    three_of_a_kind = 4
    two_pair = 3
    one_pair = 2
    high_card = 1


@dataclass
class Hand:
    cards: str
    bid: int


@dataclass
class Input:
    lines: List[str]
    hands: List[Hand]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)

    hands = []
    for line in lines:
        parts = line.split(' ')
        hands.append(Hand(parts[0], int(parts[1])))

    return Input(lines, hands)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


CARD_ORDER1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_ORDER1.reverse()


CARD_ORDER2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
CARD_ORDER2.reverse()


def hand_to_result(hand: Hand) -> HandType:
    c = sorted(hand.cards)
    if c[0] == c[1] == c[2] == c[3] == c[4]:
        return HandType.five_of_a_kind
    if (c[1] == c[2] == c[3]) and (c[0] == c[1] or c[4] == c[1]):
        return HandType.four_of_a_kind
    if ((c[0] == c[1] == c[2]) and (c[3] == c[4])) or ((c[2] == c[3] == c[4]) and (c[0] == c[1])):
        return HandType.full_house
    if (c[0] == c[1] == c[2]) or (c[2] == c[3] == c[4]) or (c[1] == c[2] == c[3]):
        return HandType.three_of_a_kind
    if (c[0] == c[1] and c[2] == c[3]) or (c[0] == c[1] and c[3] == c[4]) or (c[1] == c[2] and c[3] == c[4]):
        return HandType.two_pair
    if c[0] == c[1] or c[0] == c[2] or c[0] == c[3] or c[0] == c[4] or c[1] == c[2] or c[1] == c[3] or c[1] == c[4] or c[2] == c[3] or c[2] == c[4] or c[3] == c[4]:
        return HandType.one_pair
    return HandType.high_card


def hand_to_result2(hand: Hand) -> HandType:
    if 'J' not in hand.cards:
        return hand_to_result(hand)
    max_result = hand_to_result(hand)
    for c in CARD_ORDER2:
        if c == 'J':
            continue
        _hand = Hand(hand.cards.replace('J', c), hand.bid)
        result = hand_to_result(_hand)
        if result.value > max_result.value:
            max_result = result
    return max_result


def compare(h1: Hand, h2: Hand, card_order: List[str], result) -> int:
    r1 = result(h1)
    r2 = result(h2)
    if r1.value != r2.value:
        return (r1.value - r2.value) * 100
    for idx in range(0, 5):
        c1 = h1.cards[idx]
        c2 = h2.cards[idx]
        i1 = card_order.index(c1)
        i2 = card_order.index(c2)
        if i1 != i2:
            return i1 - i2
    return 0


def compare1(h1: Hand, h2: Hand) -> int:
    return compare(h1, h2, CARD_ORDER1, hand_to_result)


def compare2(h1: Hand, h2: Hand) -> int:
    return compare(h1, h2, CARD_ORDER1, hand_to_result2)


def total_winnings(hands: List[Hand]) -> int:
    winning_power = 0
    for idx in range(0, len(hands)):
        winning_power += (idx + 1) * hands[idx].bid
    return winning_power


@timer
def solve1(input: Input) -> Optional[int]:
    return total_winnings(sorted(input.hands, key=cmp_to_key(compare1)))


@timer
def solve2(input: Input) -> Optional[int]:
    return total_winnings(sorted(input.hands, key=cmp_to_key(compare2)))


# ==== Solutions with test data ==== #


test_data1 = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
test_answer1 = 6440

test_data2 = test_data1
test_answer2 = 5905

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
