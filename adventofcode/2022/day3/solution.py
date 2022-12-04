#!/usr/bin/env python3

from enum import Enum
from typing import List, Optional, Tuple, Union


# ==== Solutions ==== #


def score_item(char: str) -> int:
    index = ord(char)
    a = ord('a') # 97
    A = ord('A') # 65
    if index - a < 0:
        # Uppercase
        return index - A + 27
    else:
        return index - a + 1


def get_rucksacks(data: str) -> List[Tuple[str, str]]:
    rucksacks = []
    for line in data.splitlines():
        if not line:
            continue
        mid = int(len(line) / 2)
        rucksacks.append((line[0:mid], line[mid:]))
    return rucksacks


def find_common_item(rucksack: Tuple[str, str]) -> Optional[str]:
    for c in rucksack[0]:
        if c in rucksack[1]:
            return c
    raise ValueError('Cannot find common item')


def get_groups(data: str) -> List[Tuple[str, str, str]]:
    groups = []
    rucksack = []
    for line in data.splitlines():
        if not line:
            continue
        rucksack.append(line)
        if len(rucksack) == 3:
            groups.append(tuple(rucksack))
            rucksack = []
    return groups


def find_common_item_in_group(group: Tuple[str, str, str]):
    common = set(group[0]).intersection(set(group[1]), set(group[2]))
    return common.pop()

def solve1(data: str) -> Optional[int]:
    score = 0
    for rucksack in get_rucksacks(data):
        item = find_common_item(rucksack)
        score += score_item(item)
    return score


def solve2(data: str) -> Optional[int]:
    score = 0
    for group in get_groups(data):
        common = find_common_item_in_group(group)
        score += score_item(common)
    return score


# ==== Solutions with test data ==== #


test_data1 = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
test_answer1 = 157

test_data2 = test_data1
test_answer2 = 70

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
