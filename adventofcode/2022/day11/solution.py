from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
import numpy as np


sys.set_int_max_str_digits(4300)


# === Useful Functions === #


def splitlines(data: str, func=lambda x: x) -> List[str]:
    return [func(line) for line in data.splitlines() if line]


@dataclass
class Operation:
    left: str
    right: str
    op: str

    def calculate(self, worry: Worry):
        if self.right == 'old':
            worry.multiply_self()
            return
        right = int(self.right)
        if self.op == '*':
            worry.multiply(right)
        elif self.op == '+':
            worry.plus(right)
        else:
            raise ValueError(
                f'Unknown equation: {self.left} {self.op} {self.right}')


class Worry:
    def __init__(self, val: int, precise: bool) -> None:
        self.precise = precise
        if not precise:
            tests = [2, 3, 5, 7, 11, 13, 17, 19, 23]
            self.r: Dict[int, int] = {}
            for test in tests:
                self.r[test] = val % test
        else:
            self.val = val
    
    def divide_by_three(self):
        self.val //= 3

    def plus(self, target: int):
        if self.precise:
            self.val += target
        else:
            for div, value in self.r.items():
                target_r = target % div
                self.r[div] = (value + target_r) % div

    def multiply(self, target: int):
        if self.precise:
            self.val *= target
        else:
            for div, value in self.r.items():
                target_r = target % div
                self.r[div] = (value * target_r) % div

    def multiply_self(self):
        if self.precise:
            self.val *= self.val
        else:
            for div, value in self.r.items():
                self.r[div] = (value * value) % div

    def divisible_by(self, target: int) -> bool:
        if self.precise:
            return self.val % target == 0
        else:
            return self.r[target] == 0


@dataclass
class Monkey:
    items: List[Worry]
    op: Operation
    test: int
    true_monkey: int
    false_monkey: int


@dataclass
class Input:
    monkeys: List[Monkey]


# === Input parsing === #


def parse_input(data: str, precise: bool) -> Input:
    monkeys = []
    items: List[Worry] = []
    op = Operation('0', '0', '?')
    test = 0
    true_monkey = 0
    false_monkey = 0
    for line in data.splitlines():
        if 'Starting items:' in line:
            # '  Starting items: 79, 98'
            items = [Worry(int(item), precise) for item in line[18:].split(', ')]
        elif 'Operation:' in line:
            # '  Operation: new = old * 19'
            tokens = line[19:].split(' ')
            op = Operation(tokens[0], tokens[2], tokens[1])
        elif 'Test:' in line:
            # '  Test: divisible by 23
            test = int(line[21:])
        elif 'If true:' in line:
            # '    If true: throw to monkey 2'
            true_monkey = int(line[29:])
        elif 'If false:' in line:
            # '    If false: throw to monkey 3'
            false_monkey = int(line[30:])
            monkeys.append(Monkey(items, op, test, true_monkey, false_monkey))
        else:
            pass

    return Input(monkeys)


def parse_input1(data: str) -> Input:
    return parse_input(data, precise=True)


def parse_input2(data: str) -> Input:
    return parse_input(data, precise=False)


# === Solutions === #


def solve1(input: Input) -> Optional[int]:
    monkeys = input.monkeys
    monkey_activities = [0 for _ in monkeys]
    for _ in range(0, 20):
        for index, monkey in enumerate(monkeys):
            for worry in monkey.items:
                monkey_activities[index] += 1
                monkey.op.calculate(worry)
                worry.divide_by_three()
                if worry.divisible_by(monkey.test):
                    monkeys[monkey.true_monkey].items.append(worry)
                else:
                    monkeys[monkey.false_monkey].items.append(worry)
                monkeys[index].items = []
    monkey_activities.sort(reverse=True)
    return monkey_activities[0] * monkey_activities[1]


def solve2(input: Input) -> Optional[int]:
    monkeys = input.monkeys
    monkey_activities = [0 for _ in monkeys]
    for round in range(0, 10000):
        for index, monkey in enumerate(monkeys):
            for worry in monkey.items:
                monkey_activities[index] += 1
                monkey.op.calculate(worry)
                if worry.divisible_by(monkey.test):
                    monkeys[monkey.true_monkey].items.append(worry)
                else:
                    monkeys[monkey.false_monkey].items.append(worry)
                monkeys[index].items = []
    monkey_activities.sort(reverse=True)
    return monkey_activities[0] * monkey_activities[1]


# ==== Solutions with test data ==== #


test_data1 = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
test_answer1 = 10605

test_data2 = test_data1
test_answer2 = 2713310158

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
