#!/usr/bin/env python3

from typing import List, Optional, Union


# ==== Solutions ==== #


def get_elves(data: str) -> dict:
    lines = data.splitlines()
    elves = []
    elf = []
    for line in lines:
        if not line and len(elf) > 0:
            elves.append(elf)
            elf = []
        else:
            elf.append(int(line))
    if len(elf) > 0:
        elves.append(elf)
    return elves


def count_callories(elves: List[List[int]]) -> List[int]:
    callories = []
    for elf in elves:
        count = 0
        for callory in elf:
            count += callory
        callories.append(count)
    return callories


def solve1(data: str) -> Optional[int]:
    elves = get_elves(data)
    callories = count_callories(elves)
    return max(callories)


def solve2(data: str) -> Optional[int]:
    elves = get_elves(data)
    callories = count_callories(elves)
    callories.sort(reverse=True)
    return callories[0] + callories[1] + callories[2]


# ==== Solutions with test data ==== #


test_data1 = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
test_answer1 = 24000

test_data2 = test_data1
test_answer2 = 45000

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
