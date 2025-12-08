from functools import reduce
from typing import List

from framework import run_solutions

# Configuration
DAY = 8
SAMPLE_ANSWER1 = 40
SAMPLE_ANSWER2 = 40


# Solutions
def solve1(input: str) -> int:
    boxes = parse(input)
    union_ops_count = 10 if len(boxes) < 100 else 1000

    # Prepare graph.
    nodes = list(zip(range(0, len(boxes)), boxes))
    edges = []
    for i in range(0, len(boxes) - 1):
        for j in range(i + 1, len(boxes)):
            edges.append((i, j, distance(boxes[i], boxes[j])))
    edges.sort(key=lambda edge: edge[2])

    # Perform union operations.
    union_ops = [(edge[0], edge[1]) for edge in edges[0:union_ops_count]]
    for (p, q) in union_ops:
        p_id = nodes[p][0]
        q_id = nodes[q][0]
        if p_id == q_id:
            continue
        for i in range(0, len(nodes)):
            if nodes[i][0] == p_id:
                nodes[i] = (q_id, nodes[i][1])

    # Find number of connections
    connections = {}
    for id, _ in nodes:
        if id in connections:
            connections[id] += 1
        else:
            connections[id] = 1
    connections = sorted(connections.values(), reverse=True)

    return reduce(lambda prev, curr: prev * curr, connections[0:3], 1)


def solve2(input: str) -> int:
    return 0


def distance(a, b) -> float:
    [ax, ay, az] = a
    [bx, by, bz] = b
    return ((ax - bx)**2 + (ay - by)**2 + (az - bz)**2)**0.5


def parse(input: str) -> List[List[int]]:
    return [[int(number) for number in line.split(',')] for line in input.splitlines()]


# Run solutions
run_solutions(DAY, (solve1, solve2), (SAMPLE_ANSWER1, SAMPLE_ANSWER2))
