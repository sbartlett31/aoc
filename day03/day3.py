from collections import Counter
from itertools import *
import more_itertools
from typing import *
import cytoolz as toolz


def main() -> None:
    data = read_input()
    part1(data)
    part2(data)


def read_input(fp="./input") -> List[str]:
    return open(fp).read().splitlines()


def get_duped_items(knapsack: str) -> str:
    midpoint = len(knapsack) // 2
    s1 = set(knapsack[:midpoint])
    s2 = set(knapsack[midpoint:])
    return s1.intersection(s2).pop()


def get_priority(char: str) -> int:
    if ord(char) < 97:
        return ord(char) - 38
    return ord(char) - 96


def get_group_items(knapsacks: List[str]) -> List[str]:
    return [get_common_item(group) for group in more_itertools.chunked(knapsacks, 3)]


def get_common_item(knapsacks: List[str]) -> str:
    return toolz.pipe(
        map(set, knapsacks),
        toolz.curried.reduce(lambda l, r: l.intersection(r)),
        set.pop,
    )


part1 = toolz.compose(
    print, sum, toolz.curried.map(get_priority), toolz.curried.map(get_duped_items)
)
part2 = toolz.compose(print, sum, toolz.curried.map(get_priority), get_group_items)

if __name__ == "__main__":
    main()
