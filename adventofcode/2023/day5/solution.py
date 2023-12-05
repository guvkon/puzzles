from __future__ import annotations

import numpy as np
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict, Set, Callable
from time import time_ns
from functools import wraps, cache, cached_property
from copy import copy


# === Useful Functions === #


def splitlines(data: str, fun=lambda x: x) -> List[str]:
    return [fun(line) for line in data.splitlines() if line]


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time_ns()
        result = f(*args, **kwargs)
        delta = (time_ns() - start) / 1000000.0
        print(f'Elapsed time of {f.__name__}: {delta} ms')
        return result

    return wrapper


# === Types === #


@dataclass
class Range:
    destination: int
    source: int
    length: int


@dataclass
class Vector:
    start: int
    length: int

    @cached_property
    def end(self) -> int:
        return self.start + self.length - 1


@dataclass
class Transformer:
    fr: str
    to: str
    ranges: List[Range]


@dataclass
class Input:
    lines: List[str]
    seeds: List[int]
    maps: List[Transformer]


# === Input parsing === #


@timer
def parse_input(data: str, options: dict) -> Input:
    lines = splitlines(data)
    result = re.match(r'seeds: (.+)', lines[0])
    seeds = [int(s.strip()) for s in result[1].split(' ') if s]
    maps = []
    just_started = True
    for idx in range(1, len(lines)):
        line = lines[idx]
        if 'map' in line:
            if just_started:
                just_started = False
            else:
                maps.append(Transformer(fr, to, ranges))

            _map = re.match(r'(\w+)-to-(\w+) map:', line)
            fr = _map[1]
            to = _map[2]
            ranges = []
            continue
        parts = [int(p.strip()) for p in line.split(' ') if p]
        ranges.append(Range(parts[0], parts[1], parts[2]))
    maps.append(Transformer(fr, to, ranges))
    return Input(lines, seeds, maps)


def parse_input1(data: str) -> Input:
    return parse_input(data, options={})


def parse_input2(data: str) -> Input:
    return parse_input(data, options={})


# === Solutions === #


def map_value(map: Transformer, value: int) -> int:
    for range in map.ranges:
        if range.source <= value <= range.source + range.length:
            return range.destination + value - range.source
    return value


def intersect(v1: Vector, v2: Vector) -> Optional[Vector]:
    if v1.start >= v2.start and v1.end <= v2.end:
        return copy(v1)
    if v2.start >= v1.start and v2.end <= v1.end:
        return copy(v2)
    if v1.end < v2.start or v1.start > v2.end:
        return None
    # v1 left to v2
    if v1.start < v2.start <= v1.end < v2.end:
        start = v2.start
        end = v1.end
        return Vector(start, end - start + 1)
    # v2 left to v2
    if v2.start < v1.start <= v2.end < v1.end:
        start = v1.start
        end = v2.end
        return Vector(start, end - start + 1)
    raise ValueError(f"Uncounted for leaf. v1 = {v1, v1.end}, v2 = {v2, v2.end}")


def sort_vectors(vectors: List[Vector]) -> List[Vector]:
    return sorted(vectors, key=lambda v: v.start)


def sum_vectors(vectors: List[Vector]) -> int:
    sum = 0
    for vector in vectors:
        sum += vector.length
    return sum


def map_vector(map: Transformer, vector: Vector) -> List[Vector]:
    output = []
    mapped_vector = []
    for _range in map.ranges:
        source = intersect(Vector(_range.source, _range.length), vector)
        if source is None:
            continue
        mapped_vector.append(source)
        output.append(Vector(_range.destination + source.start - _range.source, source.length))
    if not output:
        return [vector]

    total_length = sum_vectors(output)
    if vector.length == total_length:
        return output

    if vector.length < total_length:
        raise ValueError('Mapped vectors are too large.')

    mapped_vector = sort_vectors(mapped_vector)

    if mapped_vector[0].start > vector.start:
        start = vector.start
        end = mapped_vector[0].start - 1
        _v = Vector(start, end - start + 1)
        output.append(_v)

    for idx in range(1, len(mapped_vector)):
        prev = mapped_vector[idx - 1]
        curr = mapped_vector[idx]
        start = prev.end + 1
        end = curr.start - 1
        length = end - start + 1
        if length > 0:
            _v = Vector(start, length)
            print(f'Added in loop between {prev} and {curr} = {_v}')
            output.append(_v)

    last_idx = len(mapped_vector) - 1
    if mapped_vector[last_idx].end < vector.end:
        start = mapped_vector[last_idx].end + 1
        end = vector.end
        _v = Vector(start, end - start + 1)
        print(f'Added at the end {_v}')
        output.append(_v)

    total_length = sum_vectors(output)
    if vector.length != total_length:
        raise ValueError(f'Total output is incorrect. Vector = {vector}, output = {output}')

    return output


@timer
def solve1(input: Input) -> Optional[int]:
    location = None
    for seed in input.seeds:
        category = 'seed'
        value = seed
        while category != 'location':
            for map in input.maps:
                if map.fr != category:
                    continue
                value = map_value(map, value)
                category = map.to
        if location is None or location > value:
            location = value
    return location


@timer
def solve2(input: Input) -> Optional[int]:
    location = None
    for s in range(0, len(input.seeds) // 2):
        left = input.seeds[s * 2]
        right = input.seeds[s * 2 + 1]
        seed = Vector(left, right)
        print(f'Seed = {seed}')
        values = [seed]
        for map in input.maps:
            new_values = []
            for value in values:
                _values = map_vector(map, value)
                for _value in _values:
                    new_values.append(_value)
            values = new_values
        sorted_values = sort_vectors(values)
        value = sorted_values[0].start
        print(f'Location candidates = {sorted_values}')
        if location is None or location > value:
            location = value
    return location


# ==== Solutions with test data ==== #


test_data1 = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
test_answer1 = 35

test_data2 = test_data1
test_answer2 = 46

solves = [
    {'func': solve1, 'parse': parse_input1,
     'test_data': test_data1, 'test_answer': test_answer1},
    {'func': solve2, 'parse': parse_input2,
     'test_data': test_data2, 'test_answer': test_answer2},
]


# ==== Template for running solutions ==== #


@timer
def main():
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


if __name__ == '__main__':
    main()
