from framework import run_solutions

# Configuration
DAY = 9
SAMPLE_ANSWER1 = 50
SAMPLE_ANSWER2 = 24


# Solutions
def solve1(input: str) -> int:
    reds = parse(input)
    largest = 0
    for i in range(0, len(reds) - 1):
        [ax, ay] = reds[i]
        for j in range(i + 1, len(reds)):
            [bx, by] = reds[j]
            area = (abs(bx - ax) + 1) * (abs(by - ay) + 1)
            largest = max(largest, area)
    return largest


def solve2(input: str) -> int:
    return 0


def parse(input: str):
    return [[int(number) for number in line.split(',')] for line in input.splitlines()]


# Run solutions
run_solutions(DAY, (solve1, solve2), (SAMPLE_ANSWER1, SAMPLE_ANSWER2))
