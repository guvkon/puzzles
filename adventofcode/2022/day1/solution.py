#!/usr/bin/env python3

from typing import Optional, Union


# ==== Solutions ==== #


def solve1(data: str) -> Optional[int]:
    return None


def solve2(data: str) -> Optional[int]:
    return None


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
test_answer2 = 24000

solves = [
    {'func': solve1, 'test_data': test_data1, 'test_answer': test_answer1},
    # {'func': solve2, 'test_data': test_data2, 'test_answer': test_answer2},
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
