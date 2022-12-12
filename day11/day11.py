from collections import *
from typing import *
import dataclasses
import cytoolz as toolz
import re
import typer
from pprint import pprint
from functools import reduce
import operator


@dataclasses.dataclass
class Monkey:
    number: int
    items: Deque[int]
    operation: Callable[[int], int]
    divisor: int
    monkey_if_true: int
    monkey_if_false: int
    orig_text: str
    num_inspected: int = 0

    @classmethod
    def from_crappy_input(cls, txt: str) -> "Monkey":
        lines = txt.splitlines()
        number = int(re.search(r"\d+", lines[0]).group(0))
        items = toolz.pipe(re.findall(r"\d+", lines[1]), toolz.curried.map(int), deque)
        operation = cls.get_operation_from_txt(lines[2])
        monkey_if_true = int(re.search(r"\d+", lines[4]).group(0))
        monkey_if_false = int(re.search(r"\d+", lines[5]).group(0))
        divisor_line = lines[3]
        divisor_val = int(divisor_line.split()[-1])

        return cls(
            number, items, operation, divisor_val, monkey_if_true, monkey_if_false, txt
        )

    def test(self, x: int) -> bool:
        return (x % self.divisor) == 0

    @staticmethod
    def get_operation_from_txt(line: str) -> Callable[[int], int]:
        func = line.split(" = ")[-1]

        def disgusting(old):
            return eval(func.replace("old", str(old)))

        return disgusting


def parse_input(fp: "./input") -> List[Monkey]:
    with open(fp) as f:
        txt = f.read()
    txt_monkeys = txt.split("\n\n")
    monkey_dict = {
        k: Monkey.from_crappy_input(monkey_txt)
        for k, monkey_txt in enumerate(txt_monkeys)
    }
    return monkey_dict


def take_turn(monkey_dict: Dict[int, Monkey], monkey: Monkey, worry_divisor, item_deflator):
    if not monkey.items:
        return
    while monkey.items:
        item = monkey.items.popleft()
        monkey.num_inspected += 1
        item = monkey.operation(item)
        item = item // worry_divisor
        if monkey.test(item):
            monkey_dict[monkey.monkey_if_true].items.append(item % item_deflator)
        else:
            monkey_dict[monkey.monkey_if_false].items.append(item % item_deflator)
    return


def play_round(monkey_dict, worry_divisor: int, item_deflator:int) -> None:
    for monkey in monkey_dict.values():
        take_turn(monkey_dict, monkey, worry_divisor=worry_divisor, item_deflator=item_deflator)


def get_modulo_value(monkey_dict):
    """wtf is this rsa?"""
    return reduce(operator.mul, (m.divisor for m in monkey_dict.values()))

def main(fp: str):
    monkey_dict = parse_input(fp)
    item_deflator = get_modulo_value(monkey_dict)

    for i in range(20):
        print(f'playing round {i}')
        play_round(monkey_dict, worry_divisor=3, item_deflator=item_deflator)
    nums_inspected = sorted([v.num_inspected for v in monkey_dict.values()])
    print(nums_inspected[-1] * nums_inspected[-2])

    monkey_dict = parse_input(fp)
    for i in range(10_000):
        if not i % 1000:
            print(f'playing round {i}')
        play_round(monkey_dict, worry_divisor=1, item_deflator=item_deflator)
    nums_inspected = sorted([v.num_inspected for v in monkey_dict.values()])
    print(nums_inspected)
    print(nums_inspected[-1] * nums_inspected[-2])


if __name__ == "__main__":
    typer.run(main)
