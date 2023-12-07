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


class CardCombination(Enum):
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


CARD_ORDER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_ORDER.reverse()


CARD_ORDER_WITH_JOKER = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
CARD_ORDER_WITH_JOKER.reverse()


@cache
def cards_combination(cards: str) -> CardCombination:
    d = {}
    for c in cards:
        d[c] = d.get(c, 0) + 1
    groups = sorted(list(d.values()), reverse=True)

    if groups == [5]:
        return CardCombination.five_of_a_kind
    if groups == [4, 1]:
        return CardCombination.four_of_a_kind
    if groups == [3, 2]:
        return CardCombination.full_house
    if groups == [3, 1, 1]:
        return CardCombination.three_of_a_kind
    if groups == [2, 2, 1]:
        return CardCombination.two_pair
    if groups == [2, 1, 1, 1]:
        return CardCombination.one_pair
    return CardCombination.high_card


def hand_combination(hand: Hand) -> CardCombination:
    return cards_combination(hand.cards)


def hand_combination_with_joker(hand: Hand) -> CardCombination:
    if 'J' not in hand.cards:
        return hand_combination(hand)
    max_combination = cards_combination(hand.cards)
    for c in hand.cards:
        if c == 'J':
            continue
        result = cards_combination(hand.cards.replace('J', c))
        if result.value > max_combination.value:
            max_combination = result
    return max_combination


def generic_compare(h1: Hand, h2: Hand, card_order: List[str], result) -> int:
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


def compare(h1: Hand, h2: Hand) -> int:
    return generic_compare(h1, h2, CARD_ORDER, hand_combination)


def compare_with_joker(h1: Hand, h2: Hand) -> int:
    return generic_compare(h1, h2, CARD_ORDER_WITH_JOKER, hand_combination_with_joker)


def total_winnings(hands: List[Hand]) -> int:
    winning_power = 0
    for idx in range(0, len(hands)):
        winning_power += (idx + 1) * hands[idx].bid
    return winning_power


@timer
def solve1(input: Input) -> Optional[int]:
    return total_winnings(sorted(input.hands, key=cmp_to_key(compare)))


@timer
def solve2(input: Input) -> Optional[int]:
    return total_winnings(sorted(input.hands, key=cmp_to_key(compare_with_joker)))


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
    start = time_ns()
    filename = 'input.txt'
    with open(filename, 'r') as f:
        input = f.read()
        delta = (time_ns() - start) / 1000000.0
        print(f'Elapsed time of reading file: {delta} ms')

        number = 1
        for solve in solves:
            func = solve['func']
            parse = solve['parse']

            slv = func(parse(solve['test_data']))
            answer = solve['test_answer']
            if slv == answer:
                print()
                print(f'Solution {number} - Test has passed')
                print()
            else:
                print()
                print(
                    f'Solution {number} - Test has failed. Should be:\n{answer}\nGot:\n{slv}')
                print()
                number += 1
                continue

            slv = func(parse(input))
            if slv is not None:
                print()
                print(f'Solution {number} - The answer is {slv}')
                print()
            number += 1


if __name__ == '__main__':
    main()
