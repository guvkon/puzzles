from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union, Dict


# === Useful Functions === #


def splitlines(data: str, func=lambda x: x) -> List[str]:
    return [func(line) for line in data.splitlines() if line]


# ==== Types ==== #


@dataclass
class Command:
    cmd: str
    arg: Optional[str]


@dataclass
class Output:
    cmd: Command
    output: List[str]


@dataclass
class Input:
    outputs: List[Output]


@dataclass
class Node:
    name: str
    parent: Optional[Node]
    size: Optional[int]
    children: Optional[List[Node]]


@dataclass
class File(Node):
    size: int
    children: None


@dataclass
class Directory(Node):
    children: List[Node]


# === Input parsing === #


def parse_input(data: str) -> Input:
    outputs = []
    output = None
    for line in splitlines(data):
        is_command = line[0] == '$'
        if is_command:
            parts = line[2:].split(' ')
            cmd = Command(parts[0], parts[1] if len(parts) > 1 else None)
            output =  Output(cmd, [])
            outputs.append(output)
        elif output is not None:
            output.output.append(line)
    return Input(outputs)


def parse_input1(data: str) -> Input:
    return parse_input(data)


def parse_input2(data: str) -> Input:
    return parse_input(data)


# === Solutions === #


def pwd2str(pwd: List[str]) -> str:
    return '/' + '/'.join(pwd)
    


def build_directory_tree(outputs: List[Output]) -> Dict[str, Directory]:
    root = Directory('/', None, None, [])
    tree: Dict[str, Directory] = {'/': root}
    pwd = []
    for output in outputs:
        cmd = output.cmd
        if cmd.cmd == 'cd' and cmd.arg:
            if cmd.arg == '/':
                pwd = []
            elif cmd.arg == '..':
                if len(pwd) > 0:
                    pwd.pop()
            else:
                prev_dir = tree[pwd2str(pwd)]
                pwd.append(cmd.arg)
                if pwd2str(pwd) not in tree:
                    curr_dir = Directory(cmd.arg, prev_dir, None, [])
                    prev_dir.children.append(curr_dir)
                    tree[pwd2str(pwd)] = curr_dir
        elif cmd.cmd == 'ls':
            curr_dir = tree[pwd2str(pwd)]
            for line in output.output:
                parts = line.split(' ')
                if parts[0] == 'dir':
                    dir_pwd = pwd.copy()
                    dir_pwd.append(parts[1])
                    if pwd2str(dir_pwd) not in tree:
                        dir = Directory(parts[1], curr_dir, None, [])
                        curr_dir.children.append(dir)
                        tree[pwd2str(dir_pwd)] = dir
                else:
                    file = File(parts[1], curr_dir, int(parts[0]), None)
                    curr_dir.children.append(file)
    return tree


def calculate_size(node: Node) -> int:
    if node.size:
        return node.size
    if not node.children:
        return 0
    node.size = 0
    for child in node.children:
        node.size += calculate_size(child)
    return node.size



def solve1(input: Input) -> Optional[int]:
    tree = build_directory_tree(input.outputs)
    calculate_size(tree['/'])
    # Calculate solution
    score = 0
    for dir in tree.values():
        size = dir.size or 0
        if size <= 100000:
            score += size
    return score


def solve2(input: Input) -> Optional[int]:
    tree = build_directory_tree(input.outputs)
    calculate_size(tree['/'])
    total_space = 70000000
    free_space = total_space - (tree['/'].size or 0)
    update_space = 30000000
    required_space = update_space - free_space
    big_enough_sizes = []
    for dir in tree.values():
        size = dir.size or 0
        if size >= required_space:
            big_enough_sizes.append(size)
    return min(big_enough_sizes)


# ==== Solutions with test data ==== #


test_data1 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
test_answer1 = 95437

test_data2 = test_data1
test_answer2 = 24933642

solves = [
    {'func': solve1, 'parse': parse_input1, 'test_data': test_data1, 'test_answer': test_answer1},
    {'func': solve2, 'parse': parse_input2, 'test_data': test_data2, 'test_answer': test_answer2},
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
                    f'Solution {number} - Test has failed. Should be {answer}, got {slv}')
                number += 1
                continue

            slv = func(parse(input))
            if slv is not None:
                print(f'Solution {number} - The answer: {slv}')
            number += 1
