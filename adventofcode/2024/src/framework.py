from time import process_time_ns
from typing import Tuple


def run_solutions(day: int, solves, answers: Tuple[int, int], parts: int = 2):
    # Load inputs
    with open(f'input/day{day}_sample.txt', 'r') as f:
        input_sample = f.read()

    with open(f'input/day{day}.txt', 'r') as f:
        input = f.read()

    def run_part(part: int):
        answer = solves[part](input_sample)
        if answer == answers[part]:
            start = process_time_ns()
            answer = solves[part](input)
            end = process_time_ns()
            took_in_ms = (end - start) / 1000000

            print(f'Part {part+1} answer is: {answer}')
            print(f'It took %.3f ms' % took_in_ms)
        else:
            print(f'Part {part+1} answer is wrong! Should be {answers[part]}, got {answer}')

    for part in range(0, parts):
        run_part(part)
