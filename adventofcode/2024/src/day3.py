import re
from functools import reduce

from framework import run_solutions

# Configuration
DAY = 3
SAMPLE_ANSWER1 = 161
SAMPLE_ANSWER2 = 48


# Solutions
mul_regex = r'mul\((\d{1,3}),(\d{1,3})\)'

def solve1(input: str) -> int:
    matches = re.finditer(mul_regex, input)
    return reduce(lambda prev, curr: prev + int(curr[1]) * int(curr[2]), matches, 0)


def solve2(input: str) -> int:
    matches = re.finditer(r"(do(?:n't)?\(\))|(mul\(\d{1,3},\d{1,3}\))", input)
    total = 0
    is_enabled = True
    for match in matches:
        if match[0] == 'do()':
            is_enabled = True
        elif match[0] == "don't()":
            is_enabled = False
        elif is_enabled:
            digits = re.findall(mul_regex, match[0])[0]
            total += int(digits[0]) * int(digits[1])

    return total


# Run solutions
run_solutions(DAY, (solve1, solve2), (SAMPLE_ANSWER1, SAMPLE_ANSWER2))
