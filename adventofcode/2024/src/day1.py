from functools import reduce

from framework import run_solutions

# Configuration
DAY = 1
SAMPLE_ANSWER1 = 11
SAMPLE_ANSWER2 = 31


# Solutions
def solve1(input: str) -> int:
    lefts, rights = parse(input)
    return reduce(lambda prev, curr: prev + abs(curr[0] - curr[1]), zip(lefts, rights), 0)


def solve2(input: str) -> int:
    lefts, rights = parse(input)
    return reduce(lambda prev, curr: prev + (curr * rights.count(curr)), lefts, 0)


def parse(input: str):
    pairs = [line.split('   ') for line in input.splitlines()]
    lefts = sorted([int(pair[0]) for pair in pairs])
    rights = sorted([int(pair[1]) for pair in pairs])

    return lefts, rights


# Run solutions
run_solutions(DAY, (solve1, solve2), (SAMPLE_ANSWER1, SAMPLE_ANSWER2))
