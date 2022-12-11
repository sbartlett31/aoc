from typing import *
import re
import copy
from pprint import pprint
from more_itertools import chunked


def parse_input(fp="./input") -> Tuple[str, str]:
    res = open(fp).read().split("\n\n")
    return res


def parse_instruction(line: str) -> Tuple[int, int, int]:
    return list(map(int, re.findall(r"\d+", line)))


def parse_initial_position(txt: str) -> List[List[int]]:
    stacks = [[] for _ in range(9)]
    lines = txt.splitlines()[:-1]
    for line in lines[::-1]:
        for i, chunk in enumerate(chunked(line, 4)):
            if chunk[1] != " ":
                stacks[i].append(chunk[1])
    return stacks


def do_instruction(n_moved: int, from_stack: int, to_stack: int, stacks) -> None:
    from_stack -= 1
    to_stack -= 1
    for _ in range(n_moved):
        tmp = stacks[from_stack].pop()
        stacks[to_stack].append(tmp)
    return


def do_instruction_p2(n_moved: int, from_stack: int, to_stack: int, stacks) -> None:
    from_stack -= 1
    to_stack -= 1
    tmp = []
    for _ in range(n_moved):
        tmp.append(stacks[from_stack].pop())
    while tmp:
        stacks[to_stack].append(tmp.pop())
    return


if __name__ == "__main__":
    stack_input, instructions = parse_input()
    stacks = parse_initial_position(stack_input)
    initial_stacks = copy.deepcopy(stacks)
    pprint(stacks)

    parsed_instructions = list(map(parse_instruction, instructions.splitlines()))
    for n_moved, from_stack, to_stack in parsed_instructions:
        do_instruction(n_moved, from_stack, to_stack, stacks=stacks)
    print("part1:", "".join(s[-1] for s in stacks))

    for n_moved, from_stack, to_stack in parsed_instructions:
        do_instruction_p2(n_moved, from_stack, to_stack, stacks=initial_stacks)
    print("part2:", "".join(s[-1] for s in initial_stacks))
