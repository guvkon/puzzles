from functools import reduce

from framework import run_solutions

# Configuration
DAY = 8
SAMPLE_ANSWER1 = 40
SAMPLE_ANSWER2 = 25272


# Solutions
def solve1(input: str) -> int:
    boxes = parse(input)
    nodes, edges = prepare_graph(boxes)

    # Perform union operations.
    union_ops = [(a, b) for a, b, _ in edges[0:10 if len(boxes) < 100 else 1000]]
    for (p, q) in union_ops:
        union(p, q, nodes)

    # Find number of connections
    connections = {}
    for id, _ in nodes:
        connections[id] = connections[id] + 1 if id in connections else 1
    connections = sorted(connections.values(), reverse=True)

    return reduce(lambda prev, curr: prev * curr, connections[0:3], 1)


def solve2(input: str) -> int:
    boxes = parse(input)
    nodes, edges = prepare_graph(boxes)
    box1, box2 = get_last_connected(nodes, edges)

    return box1[0] * box2[0]


def get_last_connected(nodes, edges):
    union_ops = [(edge[0], edge[1]) for edge in edges]
    for (p, q) in union_ops:
        union(p, q, nodes)
        if is_all_connected(nodes):
            return nodes[p][1], nodes[q][1]
    raise Exception('Cannot connect everything?!')


def union(p, q, nodes):
    p_id = nodes[p][0]
    q_id = nodes[q][0]
    if p_id == q_id: return
    for i in range(0, len(nodes)):
        if nodes[i][0] == p_id:
            nodes[i] = (q_id, nodes[i][1])


def is_all_connected(nodes):
    first_id = nodes[0][0]
    for id, _ in nodes:
        if id != first_id:
            return False
    return True


def prepare_graph(boxes):
    nodes = list(zip(range(0, len(boxes)), boxes))
    edges = []
    for i in range(0, len(boxes) - 1):
        for j in range(i + 1, len(boxes)):
            edges.append((i, j, distance(boxes[i], boxes[j])))
    return nodes, sorted(edges, key=lambda edge: edge[2])


def distance(a, b):
    [ax, ay, az] = a
    [bx, by, bz] = b
    return ((ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2) ** 0.5


def parse(input: str):
    return [[int(number) for number in line.split(',')] for line in input.splitlines()]


# Run solutions
run_solutions(DAY, (solve1, solve2), (SAMPLE_ANSWER1, SAMPLE_ANSWER2))
