#!/usr/bin/env python3

from typing import Optional, Union


def solve1(data: str) -> Optional[Union[str, int]]:
    return len(data)


def solve2(data: str) -> Optional[Union[str, int]]:
    return None


solves = [
        {'func': solve1, 'test_data': '))(((((', 'test_answer': 3},
        {'func': solve2, 'test_data': '()())', 'test_answer': 5},
]


if __name__ == '__main__':
    filename = 'input.txt'
    with open(filename, 'r') as f:
        data = f.read()

        number = 1
        for solve in solves:
            func = solve['func']

            slv = func(solve['test_data'])
            answer = solve['test_answer']
            if slv == answer:
                print(f'Solution {number} - Test has passed.')
            else:
                print(f'Solution {number} - Test has failed. Should be {answer}, got {slv}.')
                number += 1
                continue

            slv = func(data)
            if slv is not None:
                print(f'Solution {number} - The answer: {slv}.')
            number += 1

