#!/usr/bin/env python3

from typing import Optional, Union


# ==== Solutions ==== #

def unpack_boxes(data: str) -> list[list[int]]:
    boxes = [box.strip() for box in data.splitlines()]
    return [[int(dim) for dim in box.split('x')] for box in boxes if len(box) > 0]


def solve1(data: str) -> Optional[Union[str, int]]:
    total = 0
    for l, w, h in unpack_boxes(data):
        # Total square of box
        total += 2 * (l * w + w * h + h * l)
        # And a bit extra -- the smallest square of a side
        total += min([l * w, w * h, h * l])
    return total


def solve2(data: str) -> Optional[Union[str, int]]:
    total = 0
    for l, w, h in unpack_boxes(data):
        # Strip
        total += min([2 * (l + w), 2 * (w + h), 2 * (h + l)])
        # Bow
        total += l * w * h
    return total


# ==== Solutions with test data ==== #


test_data1 = """2x3x4

1x1x10"""
test_answer1 = 101

test_data2 = test_data1
test_answer2 = 48

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
                print(f'Solution {number} - Test has failed. Should be {answer}, got {slv}')
                number += 1
                continue
            
            slv = func(input)
            if slv is not None:
                print(f'Solution {number} - The answer: {slv}')
            number += 1
