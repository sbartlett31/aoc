import typer
from typing import *
import cytoolz as toolz
from pprint import pprint


Command = Union[Tuple[str, int], str]


def read_input(fp="./input") -> List[Command]:
    with open(fp) as f:
        return toolz.pipe(f.read().splitlines(), toolz.curried.map(str.split), list)


def should_check(cycle: int) -> bool:
    return cycle == 20 or not (cycle - 20) % 40


def get_signal_strengths(
    data: List[Command], check_fn: Callable[[int], bool] = should_check
) -> List[str]:
    x_register = 1
    cycle: int = 0
    res = []
    screen = Screen()
    for cmd in data:
        if cmd[0] == "noop":
            cycle += 1
            screen.run_cycle(cycle, x_register)
            if check_fn(cycle):
                res.append(x_register * cycle)
        elif cmd[0] == "addx":
            for _ in range(2):
                cycle += 1
                screen.run_cycle(cycle, x_register)
                if check_fn(cycle):
                    res.append(x_register * cycle)
            x_register += int(cmd[-1])
    pprint(screen)
    return res


class Screen:
    def __init__(self, n_rows: int = 6, n_cols: int = 40):
        self.display = self.draw_display(n_rows, n_cols)
        self.current_pixel = 0

    def __repr__(self):
        return "\n".join(map("".join, self.display))

    @staticmethod
    def draw_display(n_rows: int, n_cols: int) -> List[List[str]]:
        return [["."] * n_cols for _ in range(n_rows)]

    def draw_pixel(self, cycle_number: int, x_register: int) -> None:
        row = cycle_number // 40 if cycle_number < 240 else 5
        if abs(self.current_pixel - x_register) <= 1:
            self.display[row][self.current_pixel] = "#"
        return

    def run_cycle(self, cycle_number: int, x_register: int) -> None:
        self.draw_pixel(cycle_number, x_register)
        self.current_pixel = (self.current_pixel + 1) % 40


def main(fp: str):
    data = read_input(fp)
    res = get_signal_strengths(data)
    print(res)
    print(sum(res))


if __name__ == "__main__":
    typer.run(main)
