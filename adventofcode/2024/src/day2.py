from typing import List

from framework import run_solutions

# Configuration
DAY = 2
SAMPLE_ANSWER1 = 2
SAMPLE_ANSWER2 = 4


# Solutions
def solve1(input: str) -> int:
    reports = parse(input)
    return len([report for report in reports if is_safe(report)])


def solve2(input: str) -> int:
    reports = parse(input)
    return len([report for report in reports if is_safe2(report)])


def is_safe(report: List[int]) -> bool:
    is_increasing = True
    is_decreasing = True
    is_safe_diff = True

    for i in range(1, len(report)):
        prev = report[i - 1]
        curr = report[i]
        if is_increasing and curr <= prev:
            is_increasing = False
        if is_decreasing and curr >= prev:
            is_decreasing = False
        if is_safe_diff and abs(curr - prev) > 3:
            is_safe_diff = False

    return (is_increasing or is_decreasing) and is_safe_diff


def is_safe2(report: List[int]) -> bool:
    if is_safe(report):
        return True

    for index_to_remove in range(0, len(report)):
        _report = [report[i] for i in range(0, len(report)) if i != index_to_remove]
        if is_safe(_report):
            return True

    return False


def parse(input: str):
    return [[int(level) for level in line.split(' ')] for line in input.splitlines()]


# Run solutions
run_solutions(DAY, (solve1, solve2), (SAMPLE_ANSWER1, SAMPLE_ANSWER2))
